import socket


class Client:

    def __init__(self):
        self.PORT = 8080
        self.SERVER = "127.0.0.1"
        self.ADDR = (self.SERVER, self.PORT)


def Checkmessages(client):
    # read new messages from server
    data = client.recv(2024)
    if data:
        print(data.decode())

# new socket


def main():
    user = Client()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(user.ADDR)
        Checkmessages(client)
        while True:
            string = input("Your Input: ")
            print(string)
            if not string:
                print("Cannot enter empty command")
            else:
                client.send(string.encode())
                Checkmessages(client)
                if string.lower() == "exit":
                    break


if __name__ == '__main__':
    main()
