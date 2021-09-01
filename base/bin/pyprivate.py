#!/usr/bin/python
import os
import sys
import bz2
import zlib
import base64
import marshal
import py_compile
import multiprocessing


from rich.syntax import Syntax
from rich.filesize import decimal
from rich.console import Console
from rich.progress import Progress, TextColumn, SpinnerColumn


console = Console(record=True)

copyright: str = b"""# Encoded by HackerMode tool...
# Copyright: PSH-TEAM
# Follow us on telegram ( @psh_team )
"""

check = f"""with open(__file__, 'rb') as check:exit(f\"\"\"Copyright not found!\ntry write:\n\x1b[0;32m{copyright.decode()[:-1]}\x1b[0m\nin {{__file__}}\"\"\") if not ({copyright} in check.read()) else None\n""".encode()

encode = [
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
    "function",
    "zip",
    "executable", 
    "multiple",
    "layers",
]

max_length = max(len(i) for i in encode) + 1


class PyPrivate:

    def __init__(self, filename: str, model: str) -> None:
            size = __import__("size").Size
            self.path = filename
            self.model = model
            with open(filename, 'rb') as f:
                self.source = (check if model != 'pyc' else b'') + f.read()


    def get_source(self, model: str) -> None:
        if not (model in encode):
            raise AssertionError(f"No Model '{model}' !")
        if model in encode[:4]:
            source = getattr(self, "base64")(model)
        else:
            source = getattr(self, model)
        return source if type(source) == bytes else source.encode()


    def log(self, last: str, first: str=" [plum2]Encode[/plum2]", end: str="[red]✓", tap: bool=True) -> None:
        console.print(f"[blue]#[/blue]{first} [cyan]{last}[/cyan]{' '*(max_length - len(last)) if tap else ''}{end}")

    def code_eval(self, text: str) -> str:
        code = ''.join(map(lambda a: f'\{hex(ord(a))[1:]}',text))
        return f"'{code}'"


    def base64(self, model: str) -> str:
        return f"""import builtins\nimport base64\nbuiltins.exec(builtins.compile(base64.b{model[-2:]}decode({getattr(base64, 'b' + model[-2:] + 'encode')(self.source)}), "<string>", "exec"))"""

    @property
    def bz2(self) -> str:
        return f"""import builtins\nx = lambda t, m: eval(f"__import__(\'{{m}}\'){{t}}press")({bz2.compress(self.source)})\nbuiltins.exec(builtins.compile(x(".decom", "2zb"[::-1]),"string", "exec"))"""

    @property
    def zlib(self) -> str:
        return f"""import builtins\nx = lambda t, m: eval(f"__import__(\'{{m}}\'){{t}}press")({zlib.compress(self.source)})\nbuiltins.exec(builtins.compile(x(".decom", "bilz"[::-1]),"string", "exec"))"""

    @property
    def marshal(self) -> str:
        return f"""import builtins\nimport marshal as m\nbuiltins.exec(m.loads({marshal.dumps(compile(self.source, '<string>', 'exec'))}))"""

    @property
    def eval(self) -> str:
        encode = ''.join(map(lambda t: chr(eval(f'ord(t) {"-" if ord(t) + 100 > 1114111 else "+"} 100')), self.source.decode())).encode()
        return f"""import builtins\ndata = ({encode}, eval('\\x5b\\x62\\x75\\x69\\x6c\\x74\\x69\\x6e\\x73\\x2e\\x65\\x78\\x65\\x63\\x2c\\x20\\x6c\\x61\\x6d\\x62\\x64\\x61\\x20\\x63\\x3a\\x20\\x62\\x75\\x69\\x6c\\x74\\x69\\x6e\\x73\\x2e\\x63\\x6f\\x6d\\x70\\x69\\x6c\\x65\\x28\\x63\\x2c\\x20\\x27\\x3c\\x73\\x74\\x72\\x69\\x6e\\x67\\x3e\\x27\\x2c\\x20\\x27\\x65\\x78\\x65\\x63\\x27\\x29\\x2c\\x20\\x6c\\x61\\x6d\\x62\\x64\\x61\\x20\\x74\\x3a\\x20\\x63\\x68\\x72\\x28\\x28\\x6f\\x72\\x64\\x28\\x74\\x29\\x2d\\x31\\x30\\x30\\x29\\x20\\x20\\x69\\x66\\x20\\x6f\\x72\\x64\\x28\\x74\\x29\\x20\\x2b\\x20\\x31\\x30\\x30\\x20\\x3e\\x20\\x31\\x31\\x31\\x34\\x31\\x31\\x31\\x20\\x65\\x6c\\x73\\x65\\x20\\x28\\x6f\\x72\\x64\\x28\\x74\\x29\\x20\\x2d\\x20\\x31\\x30\\x30\\x29\\x29\\x2c\\x20\\x6d\\x61\\x70\\x2c\\x20\\x6c\\x61\\x6d\\x62\\x64\\x61\\x20\\x74\\x3a\\x20\\x27\\x27\\x2e\\x6a\\x6f\\x69\\x6e\\x28\\x74\\x29\\x5d'))\ndata[1][0](data[1][1](data[1][-1](data[1][-2](data[1][-3], data[0].decode()))))"""

    @property
    def eval2(self) -> str:
        code_marshal = marshal.dumps(compile(self.source, "<string>", "exec"))
        return f"""import builtins\neval({self.code_eval('builtins.exec')})(eval({self.code_eval('__import__')})(eval({self.code_eval('"marshal"')})).loads({code_marshal}))"""

    @property
    def binary(self) -> str:
        data = list(map(lambda t: int(bin(ord(t))[2:]), self.source.decode()))
        return f"""import builtins\ndata = ({data}, eval("\\x5b\\x62\\x75\\x69\\x6c\\x74\\x69\\x6e\\x73\\x2e\\x65\\x78\\x65\\x63\\x2c\\x20\\x6c\\x61\\x6d\\x62\\x64\\x61\\x20\\x63\\x3a\\x20\\x62\\x75\\x69\\x6c\\x74\\x69\\x6e\\x73\\x2e\\x63\\x6f\\x6d\\x70\\x69\\x6c\\x65\\x28\\x63\\x2c\\x20\\x27\\x3c\\x73\\x74\\x72\\x69\\x6e\\x67\\x3e\\x27\\x2c\\x20\\x27\\x65\\x78\\x65\\x63\\x27\\x29\\x2c\\x20\\x6c\\x61\\x6d\\x62\\x64\\x61\\x20\\x74\\x3a\\x20\\x63\\x68\\x72\\x28\\x69\\x6e\\x74\\x28\\x66\\x27\\x30\\x62\\x7b\\x74\\x7d\\x27\\x2c\\x20\\x32\\x29\\x29\\x2c\\x20\\x6d\\x61\\x70\\x2c\\x20\\x6c\\x61\\x6d\\x62\\x64\\x61\\x20\\x74\\x3a\\x20\\x27\\x27\\x2e\\x6a\\x6f\\x69\\x6e\\x28\\x74\\x29\\x5d"))\ndata[1][0](data[1][1](data[1][-1](data[1][-2](data[1][-3], data[0]))))"""

    @property
    def pyc(self) -> bytes:
        try:
            py_compile.compile(self.path, f"{self.path}c", doraise=True)
        except py_compile.PyCompileError as e:
            raise SyntaxError(f"{e.exc_value}")
        return b'( pyc.code )'

    @property
    def function(self) -> bytes:
        return f"""import builtins\n(lambda a: a(builtins, {self.code_eval('exec')}))(eval({self.code_eval('getattr')}))((lambda i,m: m(i({self.code_eval('marshal')}), {self.code_eval('loads')})( m(i({self.code_eval('base64')}), {self.code_eval('b64decode')})({base64.b64encode(marshal.dumps(compile(self.source, '<string>', 'exec')))})))(eval({self.code_eval('__import__')}), eval({self.code_eval('getattr')})))""".encode()

    @property
    def zip(self) -> bytes:
        code = zlib.compress(
            bz2.compress(
                marshal.dumps(
                    compile(self.source, "<string>", "exec")
                )
            )
        )
        return f"""import builtins\nbuiltins.exec(eval(getattr(getattr('', {self.code_eval('join')})(getattr(builtins, {self.code_eval('map')})(chr, [95, 95, 105, 109, 112, 111, 114, 116, 95, 95, 40, 39, 109, 97, 114, 115, 104, 97, 108, 39, 41, 46, 108, 111, 97, 100, 115, 40, 95, 95, 105, 109, 112, 111, 114, 116, 95, 95, 40, 39, 98, 122, 50, 39, 41, 46, 100, 101, 99, 111, 109, 112, 114, 101, 115, 115, 40, 95, 95, 105, 109, 112, 111, 114, 116, 95, 95, 40, 39, 122, 108, 105, 98, 39, 41, 46, 100, 101, 99, 111, 109, 112, 114, 101, 115, 115, 40, 123, 99, 111, 100, 101, 125, 41, 41, 41])), {self.code_eval('format')})(code={code})))""".encode()

    @property
    def executable(self) -> bytes:
        code = marshal.dumps(compile(self.source, "<string>", "exec"))
        length = len(code)
        plus = round(length / 2.5)
        char = lambda t: list(map(ord, t))[::-1]
        codec = [
            [f"builtins.exec(i({char('base64')}, {char('b64decode')})({{source}}))", base64.b64encode],
            [f"builtins.exec(i({char('bz2')}, {char('decompress')})({{source}}))", bz2.compress],
            [f"builtins.exec(i({char('zlib')}, {char('decompress')})({{source}}))", zlib.compress],
            [f"builtins.exec(i({char('marshal')}, {char('loads')})({{source}}))", lambda c: marshal.dumps(compile(c, '<string>', 'exec'))],
        ]
        execs = []
        index = 0
        for i in range(0, length + plus, plus):
            execs.append(
                codec[index][0].format(
                    source=codec[index][1](f'i{index} = {code[i-plus:i]}'.encode()),
                )
            )
            index += 1
        main_exec = codec[-1][0].format(
            source=codec[-1][1](f'builtins.exec(__import__("marshal").loads({" + ".join("i" + str(x) for x in range(len(codec)))}))'.encode())
        )
        return f"""import builtins\ni = lambda n, l: getattr(builtins, {self.code_eval('eval')})(getattr('', {self.code_eval('join')})(getattr(builtins, {self.code_eval('map')})(chr, [95, 95, 105, 109, 112, 111, 114, 116, 95, 95, 40, 39, *n[::-1], 39, 41, 46, *l[::-1]])))\n{chr(10).join(execs)}\n{main_exec}""".encode()
        
        

    @property
    def multiple(self) -> bytes:
        code = marshal.dumps(compile(self.source, "<string>", "exec"))
        d = len(code) // 60 # 61
        d = d if d > 0 else 1
        _range = range(0, len(code) + d, d)
        length = len(_range)
        encode = f"builtins.exec(m.loads(b''.join([{','.join(f'i{a}' for a in range(length))}])))".encode()
        for i in range(length):
            encode = f"import builtins\nimport marshal as m\ni{i}={repr(code[_range[i]-d:_range[i]])}\nbuiltins.exec(m.loads({marshal.dumps(compile(encode, '<string>', 'exec'))}))".encode()
        return encode

    @property
    def layers(self) -> bytes:
        for model in encode:
            if model not in ["bz2", "zip", "eval", "binary", "pyc", "layers"]:
                self.source = self.get_source(model)
                self.log(f"{model}")
        return self.source


    def start(self) -> None:
        source = copyright + self.get_source(self.model)
        if self.model != "pyc":
            with open(self.path, "wb") as f:
                f.write(source)
        self.log(f"{self.model}")

        self.log(f"{decimal(len(source) if self.model != 'pyc' else os.path.getsize(self.path + 'c'))}", " [plum2]Size  ")
        thread = multiprocessing.Process(target=lambda : console.print(Syntax(source.decode(), "python")))
        thread.start()
        thread.join(4)
        if thread.is_alive():
            thread.kill()
            self.log("[/cyan][yellow]can't show the code because the file is to big [cyan]", first='', end='[red]!', tap=False)

        self.log("[/cyan][royal_blue1]Done[cyan] ", first="", tap=False)

    @staticmethod
    def massage() -> None:
        sort_encode = []
        for i in range(len(encode)):
            point = str(round(i/ (len(encode)-1)*100)).split(".")[0]
            sort_encode.append(f'    [blue]{" "*(3-len(point))}{point}% [cyan]{encode[i]}')
        sort_encode = '\n'.join(sort_encode)
        console.print(f"""\r[green]example:[/green]\n    [red]$ [blue]pyprivate [yellow]file.py [cyan]function\n    [red]$ [blue]pyprivate [yellow]file.py [cyan]multiple\n    [red]$ [blue]pyprivate [yellow]file.py [cyan]layers\n[green]encryption:\n{sort_encode}""")
        exit()

    @classmethod
    def main(cls, progress) -> None:
        argv = sys.argv[1:]
        if len(argv) >= 2:
            path, model, *args = argv
        else: 
            cls.massage()
        if os.path.isdir(path):
            cls.massage()
        elif not os.path.exists(path):
                console.print("[blue]#[/blue] No such file")
    
        try:
            progress.add_task("")
            pyprivate = cls(path, model)
            pyprivate.start()
        except Exception as e:
            console.print(f"[red]{e.__class__.__name__}[/red]: {str(e)}")
    
if __name__ == '__main__':
    with Progress(
        TextColumn("[cyan]Encode"),
        SpinnerColumn(spinner_name="point"),
        console=console,
        transient=True,
    ) as progress:
        PyPrivate.main(progress)
