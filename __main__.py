import os
import sys

from lib.variables import Variables
from setup import Installer


class HackerMode:
    def install(self):
        Installer.install()

        # add HackerMode shortcut...
        try:
            if (shell := os.environ.get('SHELL')):
                if shell.endswith("bash"):
                    path = os.path.join(shell.split("/bin/")[0], "etc/bash.bashrc")
                    if not os.path.exists(path):
                        path = "/etc/bash.bashrc"
                elif shell.endswith("zsh"):
                    path = os.path.join(shell.split("/bin/")[0], "etc/zsh/zshrc")
                    if not os.path.exists(path):
                        path = "/etc/zsh/zshrc"
                with open(path, "r") as f:
                    data = f.read()
                if data.find(Variables.HACKERMODE_SHORTCUT) == -1:
                    with open(path, "a") as f:
                        f.write(Variables.HACKERMODE_SHORTCUT)
        except PermissionError:
            print('# please add this shortcut:')
            print(Variables.HACKERMODE_SHORTCUT.strip())
            print("# to this file:")
            print(path)

    def check(self):
        Installer.check()

    def delete(self):
        status = input("# Do you really want to delete the tool?\n [n/y]: ").lower()
        if status in ("y", "yes", "ok", "yep"):
            Installer.delete()


if __name__ == "__main__":
    HackerMode = HackerMode()
    if len(sys.argv) > 1:
        try:
            HackerMode.__getattribute__(sys.argv[1])()
        except Exception as e:
            print(e)
    else:
        print("help msg")
