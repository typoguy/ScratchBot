from scratchbot import config
import socket


class ScratchBot:
    def __init__(self):
        self.config = config.Config()

    def send(self, input):
        input = input.encode()
        self.socket.send(input + b"\r\n")
        print(b"-> " + input)

    def join(self, input):
        if input[0] == "#":
            self.send("JOIN {}".format(input))

    def part(self, input):
        if input[0] == "#":
            self.send("PART {}".format(input))

    def connect(self):
        self.socket = socket.socket()
        self.socket.connect(
            (self.config.get("bot_ircserver"), self.config.get("bot_ircport"))
        )

        self.send("NICK {}".format(self.config.get("bot_nick")))
        self.send(
            "USER {} - - :{}".format(
                self.config.get("bot_ident"), self.config.get("bot_name")
            )
        )

    def recv(self):
        data = self.socket.recv(8192).decode()

        print(data)

        for item in data.splitlines():
            line = item.split()
            if len(line) < 2:
                continue

            # print('Debug: {}'.format(line))

            if line[0] == "PING":
                self.send("PONG {}".format(line[1]))

            if line[1] == "001":
                for chan in self.config.get("bot_autojoin"):
                    self.join(chan)
