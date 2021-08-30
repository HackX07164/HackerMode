import os
import sys
import bz2
import zlib
import base64
import marshal
import py_compile
import multiprocessing


from rich.syntax import Syntax
from rich.console import Console
from rich.progress import Progress,TextColumn, SpinnerColumn


copyright: str = b"""# Encoded by HackerMode tool...
# Copyright: PSH-TEAM
# Follow us on telegram ( @psh_team )
"""

ENCRIPTION = [
    "base64",
    "base16",
    "base32",
    "base85",
    "bz2",
    "zlib",
    "marshal",
    "eval",
    "eval2",
    "binary",
    "pyc",
    "multiple",
    "layers",
    
]


class PyPrivate:
    
    def __init__(self, filename: str, model: str) -> None:
            self.newtext = ''
            self.path = filename
            self.run_function(model)


    def run_function(self, model: str) -> None:
        assert model in ENCRIPTION
        try:
            if model.startswith("base"):
                getattr(self, "base64")(model)
            else:
                getattr(self, model)()
            print(f"\x1b[0;34m# \x1b[0;32mEncode \x1b[0;33m{model} \x1b[0;34m✓")
        except FileExistsError as e:
            print(f"\x1b[0;34m# \x1b[0;31mERROR \x1b[0;33m{model} \x1b[0;34m=> \x1b[0;31m{e.__class__.__name__}: \x1b[0;0m{str(e)}")

    def _show_code(self):
        if self.newtext:
            newtext = self.newtext.decode()
        else:
            with open(self.path, "r") as f:
                newtext = f.read()
        Console().print(Syntax(newtext, "python"))

    def show_code(self):
        thread = multiprocessing.Process(target=self._show_code)
        thread.start()
        thread.join(4)
        if thread.is_alive():
            thread.kill()
            print("\x1b[0;34m# \x1b[0;33mcan't show the code because the file is the big!")


    def code_eval(self, text: str) -> str:
        code = ''.join(map(lambda a: f'\{hex(ord(a))[1:]}',text))
        return f"'{code}'"


    def read(self) -> bytes:
        check = f"""with open(__file__, 'rb') as check:exit(f\"\"\"Copyright not found!\ntry write:\n\x1b[0;32m{copyright.decode()}\x1b[0m\nin {{__file__}}\"\"\") if not ({copyright} in check.read()) else None\n""".encode()
        with open(self.path, "rb") as f:
            return check + f.read()
    
    def write(self, newtext: bytes) -> None:
        with open(self.path, "wb") as f:
            self.newtext = (copyright + (newtext if type(newtext) == bytes else newtext.encode()))
            f.write(self.newtext)

    def base64(self, model: str) -> None:
        self.write(f"""import builtins\nimport base64\nbuiltins.exec(builtins.compile(base64.b{model[-2:]}decode({getattr(base64, 'b' + model[-2:] + 'encode')(self.read())}), "<string>", "exec"))""")

    def bz2(self) -> None:
        self.write(f"""import builtins\nx = lambda t, m: eval(f"__import__(\'{{m}}\'){{t}}press")({bz2.compress(self.read())})\nbuiltins.exec(builtins.compile(x(".decom", "2zb"[::-1]),"string", "exec"))""")
    
    def zlib(self) -> None:
        self.write(f"""import builtins\nx = lambda t, m: eval(f"__import__(\'{{m}}\'){{t}}press")({zlib.compress(self.read())})\nbuiltins.exec(builtins.compile(x(".decom", "bilz"[::-1]),"string", "exec"))""")

    def marshal(self) -> None:
        self.write(f"""import builtins\nimport marshal as m\nbuiltins.exec(m.loads({marshal.dumps(compile(self.read(), '<string>', 'exec'))}))""")
    
    def eval(self) -> None:
        encode = ''.join(map(lambda t: chr(eval(f'ord(t) {"-" if ord(t) + 100 > 1114111 else "+"} 100')), self.read().decode())).encode()
        self.write(f"""import builtins\ndata = ({encode}, eval('\\x5b\\x62\\x75\\x69\\x6c\\x74\\x69\\x6e\\x73\\x2e\\x65\\x78\\x65\\x63\\x2c\\x20\\x6c\\x61\\x6d\\x62\\x64\\x61\\x20\\x63\\x3a\\x20\\x62\\x75\\x69\\x6c\\x74\\x69\\x6e\\x73\\x2e\\x63\\x6f\\x6d\\x70\\x69\\x6c\\x65\\x28\\x63\\x2c\\x20\\x27\\x3c\\x73\\x74\\x72\\x69\\x6e\\x67\\x3e\\x27\\x2c\\x20\\x27\\x65\\x78\\x65\\x63\\x27\\x29\\x2c\\x20\\x6c\\x61\\x6d\\x62\\x64\\x61\\x20\\x74\\x3a\\x20\\x63\\x68\\x72\\x28\\x28\\x6f\\x72\\x64\\x28\\x74\\x29\\x2d\\x31\\x30\\x30\\x29\\x20\\x20\\x69\\x66\\x20\\x6f\\x72\\x64\\x28\\x74\\x29\\x20\\x2b\\x20\\x31\\x30\\x30\\x20\\x3e\\x20\\x31\\x31\\x31\\x34\\x31\\x31\\x31\\x20\\x65\\x6c\\x73\\x65\\x20\\x28\\x6f\\x72\\x64\\x28\\x74\\x29\\x20\\x2d\\x20\\x31\\x30\\x30\\x29\\x29\\x2c\\x20\\x6d\\x61\\x70\\x2c\\x20\\x6c\\x61\\x6d\\x62\\x64\\x61\\x20\\x74\\x3a\\x20\\x27\\x27\\x2e\\x6a\\x6f\\x69\\x6e\\x28\\x74\\x29\\x5d'))\ndata[1][0](data[1][1](data[1][-1](data[1][-2](data[1][-3], data[0].decode()))))""")

    def eval2(self) -> None:
        code_marshal = marshal.dumps(compile(self.read(), "<string>", "exec"))
        self.write(f"""import builtins\neval({self.code_eval('builtins.exec')})(eval({self.code_eval('__import__')})(eval({self.code_eval('"marshal"')})).loads({code_marshal}))""")

    def binary(self) -> None:
        data = list(map(lambda t: int(bin(ord(t))[2:]), self.read().decode()))
        self.write(f"""import builtins\ndata = ({data}, eval("\\x5b\\x62\\x75\\x69\\x6c\\x74\\x69\\x6e\\x73\\x2e\\x65\\x78\\x65\\x63\\x2c\\x20\\x6c\\x61\\x6d\\x62\\x64\\x61\\x20\\x63\\x3a\\x20\\x62\\x75\\x69\\x6c\\x74\\x69\\x6e\\x73\\x2e\\x63\\x6f\\x6d\\x70\\x69\\x6c\\x65\\x28\\x63\\x2c\\x20\\x27\\x3c\\x73\\x74\\x72\\x69\\x6e\\x67\\x3e\\x27\\x2c\\x20\\x27\\x65\\x78\\x65\\x63\\x27\\x29\\x2c\\x20\\x6c\\x61\\x6d\\x62\\x64\\x61\\x20\\x74\\x3a\\x20\\x63\\x68\\x72\\x28\\x69\\x6e\\x74\\x28\\x66\\x27\\x30\\x62\\x7b\\x74\\x7d\\x27\\x2c\\x20\\x32\\x29\\x29\\x2c\\x20\\x6d\\x61\\x70\\x2c\\x20\\x6c\\x61\\x6d\\x62\\x64\\x61\\x20\\x74\\x3a\\x20\\x27\\x27\\x2e\\x6a\\x6f\\x69\\x6e\\x28\\x74\\x29\\x5d"))\ndata[1][0](data[1][1](data[1][-1](data[1][-2](data[1][-3], data[0]))))""")
        
    def pyc(self) -> None:
        try:
            py_compile.compile(self.path, f"{self.path}c", doraise=True)
        except py_compile.PyCompileError as e:
            raise SyntaxError(f"{e.exc_value}")
    
    def layers(self) -> None:
        for model in ENCRIPTION:
            if model in ["base32", "bz2", "eval", "binary", "pyc", "layers"]:
                continue
            PyPrivate(self.path, model)
    
    def multiple(self) -> None:
        code = marshal.dumps(compile(self.read(), "<string>", "exec"))
        d = len(code) // 50
        d = d if d > 0 else 1
        _range = range(0, len(code) + d, d)
        encode = f"builtins.exec(m.loads(b''.join([{','.join(f'i{a}' for a in _range)}])))".encode()
        first = 0
        for index in _range:
            encode = f"import builtins\nimport marshal as m\ni{index}={repr(code[first:index])}\nbuiltins.exec(m.loads({marshal.dumps(compile(encode, '<string>', 'exec'))}))".encode()
            first = index
        self.write(encode)


def pyprivate_with_progress(path: str, model: str) -> None:
    size = __import__("size").Size
    with Progress(
        TextColumn("[progress.desciption]{task.description}"),
        SpinnerColumn(spinner_name="point"),
        transient=True,
    ) as progress:
        
        progress.add_task(f"[cyan]{model}")
        py = PyPrivate(path, model)
        print("\x1b[0;34m# \x1b[0;32mSize  ",size(path, anim=False).size)
        
    py.show_code()
    print("\x1b[0;34m# Done ✓")
        

def massage_help():
    print('\x1b[0;32mencryption:')
    for x in range(len(ENCRIPTION)):
        point = str(round(x /  (len(ENCRIPTION)-1)*100))
        print(' '*(4-len(point)) + '   \x1b[0;34m' + point + "%\x1b[0;33m", ENCRIPTION[x])
    print('\x1b[0;32mexamples:\x1b[0;33m\n    $ pyprivate file.py marshal\n    $ pyprivate path/mydir layers\n    $ pyprivate file.py bz2\n    $ pyprivate file.py lambda'.replace("pyprivate", "\x1b[0;32mpyprivate\x1b[0;33m"))
    exit()


if __name__ == "__main__":
    argv = sys.argv[1:]
    print("# Start Encryption Algorithm ...")  
    if len(argv) >= 2:
        path, model = argv[:2]
    elif len(argv) < 2:
        massage_help()
    else:
        massage_help()
    try:
        pyprivate_with_progress(path, model)
    except ModuleNotFoundError:
        exit("# No HackerMode !!!")
    except Exception as e:
        print(f'{e.__class__.__name__}: {str(e)}')
        massage_help()
        
        

