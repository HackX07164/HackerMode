import os
import sys
import bz2
import zlib
import base64
import marshal
import py_compile

from rich.console import Console
from rich.syntax import Syntax


COPYRIGHT: str = """# Encoded by HackerMode tool...
# Copyright: PSH-TEAM
# Follow us on telegram ( @psh_team )"""

RUNPY: str = f"""#!/usr/bin/python3\n{COPYRIGHT}"""

DECODE_SYNTAX = lambda _bytes: RUNPY + '\n' + base64.b64decode(_bytes).decode()

SYNTAX_ENCRYPTION: dict = {
    "bz2": b'aW1wb3J0IGJ1aWx0aW5zCnggPSBsYW1iZGEgdCwgbTogYnVpbHRpbnMuZXZhbChmIl9faW1wb3J0X18oJ3t7bX19Jyl7e3R9fXByZXNzIikoe3NvdXJjZX0pCmJ1aWx0aW5zLmV4ZWMoYnVpbHRpbnMuY29tcGlsZSh4KCIuZGVjb20iLCAiYnoyIiksInN0cmluZyIsICJleGVjIikp',
    "zlib": b'aW1wb3J0IGJ1aWx0aW5zCnggPSBsYW1iZGEgdCwgbTogYnVpbHRpbnMuZXZhbChmIl9faW1wb3J0X18oJ3t7bX19Jyl7e3R9fXByZXNzIikoe3NvdXJjZX0pCmJ1aWx0aW5zLmV4ZWMoYnVpbHRpbnMuY29tcGlsZSh4KCIuZGVjb20iLCAiemxpYiIpLCJzdHJpbmciLCAiZXhlYyIpKQ==',
    "marshal": b'aW1wb3J0IGJ1aWx0aW5zCmltcG9ydCBtYXJzaGFsIGFzIG0KYnVpbHRpbnMuZXhlYyhtLmxvYWRzKHtzb3VyY2V9KSk=',
    "eval": b'aW1wb3J0IG1hdGgKaW1wb3J0IGJ1aWx0aW5zCmRhdGEgPSAne3NvdXJjZX0nCmkgPSBidWlsdGlucy5ldmFsKGInXHg1Ylx4NmNceDYxXHg2ZFx4NjJceDY0XHg2MVx4MjBceDczXHgzYVx4MjBceDYyXHg3NVx4NjlceDZjXHg3NFx4NjlceDZlXHg3M1x4MmVceDYzXHg2Zlx4NmRceDcwXHg2OVx4NmNceDY1XHgyOFx4NzNceDJjXHgyMFx4MjdceDNjXHg3M1x4NzRceDcyXHg2OVx4NmVceDY3XHgzZVx4MjdceDJjXHgyMFx4MjdceDY1XHg3OFx4NjVceDYzXHgyN1x4MjlceDJjXHgyMFx4NjJceDc1XHg2OVx4NmNceDc0XHg2OVx4NmVceDczXHgyZVx4NjVceDc4XHg2NVx4NjNceDJjXHgyMFx4MjdceDI3XHgyZVx4NmFceDZmXHg2OVx4NmVceDJjXHgyMFx4NmRceDYxXHg3MFx4MmNceDIwXHg2Y1x4NjFceDZkXHg2Mlx4NjRceDYxXHgyMFx4NzRceDNhXHgyMFx4NjNceDY4XHg3Mlx4MjhceDY5XHg2ZVx4NzRceDI4XHg2ZFx4NjFceDc0XHg2OFx4MmVceDczXHg3MVx4NzJceDc0XHgyOFx4NmZceDcyXHg2NFx4MjhceDc0XHgyOVx4MjlceDI5XHgyOVx4NWQnKQppWzFdKGlbLTVdKGlbLTNdKGlbLTJdKGlbLTFdLCBkYXRhKSkpKQ==',
    "eval2": b'aW1wb3J0IGJ1aWx0aW5zCmJ1aWx0aW5zLmV4ZWMoYnVpbHRpbnMuZXZhbCgne3NvdXJjZX0nKSk=',
    "binary": b'aW1wb3J0IGJ1aWx0aW5zCmRhdGEgPSB7c291cmNlfQppID0gYnVpbHRpbnMuZXZhbChiJ1x4NWJceDYyXHg3NVx4NjlceDZjXHg3NFx4NjlceDZlXHg3M1x4MmVceDY1XHg3OFx4NjVceDYzXHgyY1x4MjBceDZjXHg2MVx4NmRceDYyXHg2NFx4NjFceDIwXHg3M1x4M2FceDIwXHg2Mlx4NzVceDY5XHg2Y1x4NzRceDY5XHg2ZVx4NzNceDJlXHg2M1x4NmZceDZkXHg3MFx4NjlceDZjXHg2NVx4MjhceDczXHgyY1x4MjBceDI3XHgzY1x4NzNceDc0XHg3Mlx4NjlceDZlXHg2N1x4M2VceDI3XHgyY1x4MjBceDI3XHg2NVx4NzhceDY1XHg2M1x4MjdceDI5XHgyY1x4MjBceDI3XHgyN1x4MmVceDZhXHg2Zlx4NjlceDZlXHgyY1x4MjBceDZkXHg2MVx4NzBceDJjXHgyMFx4NWJceDZjXHg2MVx4NmRceDYyXHg2NFx4NjFceDIwXHg3NFx4M2FceDIwXHg2M1x4NjhceDcyXHgyOFx4NjlceDZlXHg3NFx4MjhceDY2XHgyN1x4MzBceDYyXHg3Ylx4NzRceDdkXHgyN1x4MmNceDIwXHgzMlx4MjlceDI5XHgyY1x4MjBceDY0XHg2MVx4NzRceDYxXHg1ZFx4NWQnKQppWzBdKGlbMV0oaVsyXShpWzNdKCppWzRdKSkpKQ==',
    "pyc": None,
    "layers": b'e3NvdXJjZX0=',
}
BASE64: list = [
    "base64",
    "base16",
    "base32",
    "base85"
]

class PyPrivate:
    
    def __init__(self, path: str, model: str) -> None:
        self.size_file = __import__('size').Size
        print("# Start Encryption Algorithm ...")
        self.path = path
        self.model = model
        self.syntax: str = None
        if os.path.isdir(path):
            for _path, _dirs, _files in os.walk(path):
                for file in _files:
                    if file.endswith('.py'):
                        self.path = os.path.join(_path, file)
                        if model == "pyc":
                            self.pyc
                            print('\x1b[0m# \x1b[0;32mpyc ✓')
                        else:
                            self.source = self.reader
                            self._bytes = self.bytes
                            self.encryption
            print("\x1b[0m# \x1b[0;33mDone ✓")
            return
        else:
            if model == "pyc":
                 self.pyc
                 exit('\x1b[0m# \x1b[0;32mpyc ✓\n\x1b[0m# \x1b[0;33mDone ✓')
            self.source = self.reader
            self._bytes = self.bytes   
        self.encryption
        print("\x1b[0m# \x1b[0;33mDone ✓")
        
        
    @property
    def encryption(self) -> None:
        content_file = self.syntax.format(source=self._bytes).encode()
        with open(self.path, "wb") as f:
            f.write(content_file)
        print(f"\x1b[0m# \x1b[0;32m{self.model} ✓")
        print(f"\x1b[0;33m{self.path}\x1b[0;31m:", self.size_file(self.path).size)
        Console().print(Syntax(content_file.decode(), 'python'))
        
        
    @property
    def reader(self) -> bytes:
        check_copyright = f"""
        \rwith open(__file__, 'rb') as f:
        \r    if not ({COPYRIGHT.encode()} in f.read()):
        \r        __import__('builtins').exit(f\"\"\"Copyright not found!\ntry write:\n\x1b[0;32m{COPYRIGHT}\x1b[0m\nin {{__file__}}\"\"\")\n""".encode()
        with open(self.path, "rb") as f:
            return check_copyright + f.read()

    @property
    def bytes(self) -> bytes:
        if self.model in BASE64:
            self.syntax = DECODE_SYNTAX(b'aW1wb3J0IGJhc2U2NAppbXBvcnQgYnVpbHRpbnMKYnVpbHRpbnMuZXhlYyhidWlsdGlucy5jb21waWxlKGJhc2U2NC5ie251bX1kZWNvZGUoe3tzb3VyY2V9fSksICI8c3RyaW5nPiIsICJleGVjIikp').format(
                num=self.model[-2:]
            )
            return self.base64
        elif self.model in list(SYNTAX_ENCRYPTION.keys()):
            self.syntax = DECODE_SYNTAX(SYNTAX_ENCRYPTION[self.model])
            return eval(f"self.{self.model}")
        else:
            raise AttributeError(f"'{self.model}'")
            
    @property
    def bz2(self) -> bytes:
        return bz2.compress(self.source)

    @property
    def zlib(self) -> bytes:
        return zlib.compress(self.source)
        
    @property
    def base64(self) -> bytes:
        return eval(f"base64.b{self.model[-2:]}encode")(self.source)
    
    @property
    def marshal(self) -> bytes:
        return marshal.dumps(compile(self.source, "<string>", "exec"))

    @property
    def pyc(self) -> None:
        try:
            py_compile.compile(self.path, f"{self.path}c", doraise=True)
        except py_compile.PyCompileError as e:
            raise SyntaxError(f"{e.exc_value}")

    @property
    def layers(self) -> str:
        print(f'\x1b[0;34mlayers:')
        big_time = ['binary', 'bz2', 'eval2']
        for model in sorted(list(SYNTAX_ENCRYPTION.keys())[:-2] + BASE64):
            if model in big_time:
                print(f'  \x1b[0;31m{model} \x1b[0;34m# It takes a lot time!')
                continue
            self.model = model
            _bytes = self.bytes
            self.source = self.syntax.format(
                source=_bytes
            ).encode()
            print(f'  \x1b[0;32m{model} ✓')
        self.syntax = DECODE_SYNTAX(SYNTAX_ENCRYPTION["layers"])
        self.model = "layers"
        return self.source.decode()

    @property
    def eval(self) -> str:
        _eval = lambda : ''.join(map(lambda t: chr(ord(t)**2), self.source.decode()))
        try:
            return _eval()
        except ValueError:
            self.model = "base64"
            _bytes = self.bytes
            self.source = self.syntax.format(
                source=_bytes
            ).encode()
            self.model = "eval"
            self.syntax = DECODE_SYNTAX(SYNTAX_ENCRYPTION["eval"])
            return _eval()

    
    @property
    def eval2(self) -> str:
        m = marshal.dumps(compile(self.source, 'string', 'exec'))
        x = lambda t: ''.join(map(lambda a: f'\{hex(ord(a))[1:]}',t))
        return x(f"builtins.eval(''.join(builtins.eval(\"{x('map')}\")(builtins.eval(\"{x('chr')}\"), [95, 95, 105, 109, 112, 111, builtins.eval(\"{x('114')}\"), 116, 95, 95, 40, builtins.eval(\"{x('39')}\"), 109, 97, 114, builtins.eval(\"{x('115')}\"), 104, 97, 108, 39, 41, 46, builtins.eval(\"{x('108')}\"), 111, 97, builtins.eval(\"{x('100')}\"), 115])))({m})")


    @property
    def binary(self) -> str:
        return str(list(map(lambda t: int(bin(ord(t))[2:]), self.source.decode())))



            
            
if __name__ == "__main__":
    argv = sys.argv[1:]
    error = f"example:\n    $ pyprivate path/mytool marshal\n    $ pyprivate path/myfile eval2\n\nencryption:\n    {f'{chr(10)}    '.join(set(list(SYNTAX_ENCRYPTION.keys()) + BASE64))}"
    if len(argv) >= 2:
        path, model = argv[:2]
    elif len(argv) < 2:
        exit(error)
    else:
        exit(error)
    try:
        PyPrivate(path, model)
    except ModuleNotFoundError:
        exit("No HackerMode !!!")
    except Exception as e:
        exit(f'{e.__class__.__name__}: {str(e)}\n'+error)
