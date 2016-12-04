#!/usr/bin/env python3
from scratchbot import irc

if __name__ == "__main__":
    bot = irc.ScratchBot()
    bot.connect()

    while True:
        bot.recv()
