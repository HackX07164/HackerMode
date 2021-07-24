import sys
from setup import Installer


class HackerMode:
    def install(self):
        Installer.install()

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
