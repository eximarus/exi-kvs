import socket
from typing import Optional
from datetime import datetime, timedelta
import threading


class Item(object):
    def __init__(self, value: str, expiry: Optional[datetime]) -> None:
        self.value = value
        self.expiry = expiry


db: dict[str, Item] = {}


def add_connection(client_socket: socket.socket):
    while True:
        req = client_socket.recv(4096).decode("utf8")
        if len(req) == 0:
            break  # conneciton closed
        elif req.lower() == "+PING\r\n".lower():
            client_socket.send("+PONG\r\n".encode("utf8"))
        else:
            split = req.split("\r\n")
            ls: list[str] = []
            split_idx = 0
            if split[split_idx][0] == "*":
                arr_len = int(split[0][1:])
                split_idx += 1
                for _ in range(arr_len):
                    split_idx += 1
                    ls.append(split[split_idx])
                    split_idx += 1

                if ls[0].lower() == "ping":
                    client_socket.send("+PONG\r\n".encode("utf8"))
                if ls[0].lower() == "echo":
                    resp = f"*{len(ls) - 1}\r\n"
                    for item in ls[1:]:
                        resp += f"${len(item)}\r\n{item}\r\n"
                    client_socket.send(resp.encode("utf8"))

                elif ls[0].lower() == "set":
                    key = ls[1]
                    value = ls[2]

                    expiry: Optional[datetime] = None
                    if len(ls) > 4 and ls[3].lower() == "px":
                        ttl = int(ls[4])
                        expiry = datetime.now() + timedelta(milliseconds=ttl)

                    db[key] = Item(value, expiry)
                    client_socket.send("+OK\r\n".encode("utf8"))

                elif ls[0].lower() == "get":
                    key = ls[1]
                    item = db.get(key, None)
                    if item is None or (item.expiry is not None and item.expiry <= datetime.now()):
                        db.pop(key, None)
                        resp = "$-1\r\n".encode("utf8")
                    else:
                        value = item.value
                        resp = f"${len(value)}\r\n{value}\r\n".encode("utf8")

                    client_socket.send(resp)


def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        (client_socket, _) = server_socket.accept()
        threading.Thread(target=add_connection, args=(client_socket,)).start()


if __name__ == "__main__":
    main()
