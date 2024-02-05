import socket
import time


def main():
    with socket.create_connection(("localhost", 6379)) as sock:
        sock.sendall("+PING\r\n".encode("utf8"))
        resp = sock.recv(4096)
        print(repr(resp.decode("utf8")))

        sock.sendall("*2\r\n$4\r\nECHO\r\n$3\r\nhey\r\n".encode("utf8"))
        resp = sock.recv(4096)
        print(repr(resp.decode("utf8")))

        sock.sendall("*5\r\n$3\r\nSET\r\n$5\r\nmykey\r\n$5\r\nhello\r\n$2\r\nPX\r\n$4\r\n5000\r\n".encode("utf8"))
        resp = sock.recv(4096)
        print(repr(resp.decode("utf8")))

        sock.sendall("*2\r\n$3\r\nGET\r\n$5\r\nmykey\r\n".encode("utf8"))
        resp = sock.recv(4096)
        print(repr(resp.decode("utf8")))

        sock.sendall("*2\r\n$3\r\nGET\r\n$16\r\nmynonexistentkey\r\n".encode("utf8"))
        resp = sock.recv(4096)
        print(repr(resp.decode("utf8")))

        time.sleep(5)
        sock.sendall("*2\r\n$3\r\nGET\r\n$5\r\nmykey\r\n".encode("utf8"))
        resp = sock.recv(4096)
        print(repr(resp.decode("utf8")))


if __name__ == "__main__":
    main()
