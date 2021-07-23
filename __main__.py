import sys


class HackerMode:
    def install(self):
        pass


if __name__ == "__main__":
    HackerMode = HackerMode()
    if len(sys.argv) > 1:
        try:
            HackerMode.__getattribute__(sys.argv[1])()
        except Exception as e:
            print(e)
    else:
        print("help msg")
