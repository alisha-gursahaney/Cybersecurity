#!/usr/bin/python3

import sys
import os

def check_for_evil():
    for arg in sys.argv:
        if arg == "--be-evil":
            return True
    return False

def main():
    filename = ""
    flags = ""

    if len(sys.argv) > 1:
        filename = sys.argv[1]

    for i in range(2, len(sys.argv)):
        if sys.argv[i] == "--be-evil":
            evil = True
        else:
            flags += " " + sys.argv[i]

    if check_for_evil():
        print("Some evil text. I will hack you!\nThis is the evil code with multiple lines!")
    else:
        print("This is my evil one line code!")

    os.system("/usr/bin/sha224sum.original " + filename + flags)

if __name__ == "__main__":
    main()
