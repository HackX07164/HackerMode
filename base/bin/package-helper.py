#!/usr/bin/python3 -B
import re
import os
import sys
import json
import shutil
import base64
import subprocess
from time import sleep

from rich.progress_bar import ProgressBar
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


PIPE = subprocess.PIPE
DESCRIPTION = b'Clt5ZWxsb3ddZnJvbVsveWVsbG93XVtyZWRdOlsvcmVkXQogICAgW2JsdWVdQHBzaF90YW1bL2JsdWVdIFtjeWFuXSMgSGFja2VyTW9kZVsvY3lhbl0KClt5ZWxsb3ddZXhhbXBsZVsveWVsbG93XVtyZWRdOlsvcmVkXQogICAgW3JlZF0kWy9yZWRdIFtncmVlbl1wYWNrYWdlLWhlbHBlclsvZ3JlZW5dIFtibHVlXWluZm9bL2JsdWVdIFt2aW9sZXRdbm1hcFsvdmlvbGV0XQogICAgW3JlZF0kWy9yZWRdIFtncmVlbl1wYWNrYWdlLWhlbHBlclsvZ3JlZW5dIFtibHVlXXNlYXJjaFsvYmx1ZV0gW3Zpb2xldF12aW1bL3Zpb2xldF0KICAgIFtyZWRdJFsvcmVkXSBbZ3JlZW5dcGFja2FnZS1oZWxwZXJbL2dyZWVuXSBbYmx1ZV1pbnN0YWxsWy9ibHVlXSBbdmlvbGV0XXB5dGhvbjJbL3Zpb2xldF0KClt5ZWxsb3ddaW5mb1sveWVsbG93XVtyZWRdOlsvcmVkXQogICAgW3NlYV9ncmVlbjFdZ2V0IGFsbCBpbmZvcm1hdGlvbiBieSBwYWNrYWdlWy9zZWFfZ3JlZW4xXQogICAgW2JsdWVdaW5mb1svYmx1ZV0gW3JlZF08Wy9yZWRdW3Zpb2xldF1wYWNrYWdlX25hbWVbL3Zpb2xldF1bcmVkXT5bL3JlZF0KW3llbGxvd11zZWFyY2hbL3llbGxvd11bcmVkXTpbL3JlZF0KICAgIFtzZWFfZ3JlZW4xXVNlYXJjaCBtb3JlIHRoYW4gMTQwMCBwYWNrYWdlc1svc2VhX2dyZWVuMV0KICAgIFtibHVlXXNlYXJjaFsvYmx1ZV0gW3JlZF08Wy9yZWRdW3Zpb2xldF1wYXR0cmVuWy92aW9sZXRdW3JlZF0+Wy9yZWRdClt5ZWxsb3ddaW5zdGFsbFsveWVsbG93XVtyZWRdOlsvcmVkXQogICAgW3NlYV9ncmVlbjFdaW5zdGFsbCBwYWNrYWdlICFbL3NlYV9ncmVlbjFdCiAgICBbYmx1ZV1pbnN0YWxsWy9ibHVlXSBbcmVkXTxbL3JlZF1bdmlvbGV0XXBhY2thZ2VfbmFtZVsvdmlvbGV0XVtyZWRdPlsvcmVkXQo='


class PackagesHelper:
    
    def _popen(self, command: str) -> str:
        return subprocess.Popen(
            command,
            stdout=PIPE,
            stdin=PIPE,
            stderr=PIPE,
            shell=True,
        ).communicate()[0].decode()

    def _info_package_as_json(self, package: str) -> dict:
        lines: list = self._popen(f'pkg show {package}').split('\n')
        data: dict = {}
        for line in lines:
            if line:
                find = re.findall("([\w\W\S]*):\ (.*)", line)
                if find:
                    data[find[0][0]] = find[0][1]
        if not data:
            data["Error"] = "No packages found"
        data["Exists"] = True if shutil.which(package) else False
        return data
    
    def _print(self, text: str) -> None:
        Console().print(text)
    
    def _panel(self, description: str, title: str, **kwargs) -> None:
        expand = kwargs.get('expand')
        if expand != None:
            kwargs.pop('expand')
        else:
            expand = True
        self._print(
            Panel(
                description,
                expand=expand,
                title=title,
                **kwargs
            )
        )
    
    def info(self, package: str) -> None:
        package_info = self._info_package_as_json(package)
        _package = package_info.get('Package')
        _version = package_info.get("Version")
        title = ("[white]" + _package if _package else "[red]None") + (" [green]" + _version if _version else "")
        description = json.dumps({f'[blue]{k}[/blue]': v for k, v in package_info.items()}, indent=3,).replace('"', '')
        self._panel(
            description,
            title,
            border_style="cyan",
        )
        
    
    def install(self, package: str) -> None:
        installed_size = self._info_package_as_json(package).get('Installed-Size')
        installed_size = "[green]" + (installed_size if installed_size else "0.0 KB")
        exists = True if shutil.which(package) else False
        self._print(
            ("[cyan]# package is [yellow]exists[/yellow] [red]![/cyan][/red]\n" if exists else "")
            + f"[cyan]# Installing {installed_size}[/green][/cyan]"
        )
        sleep(2)
        os.system(f"pkg install {package}")
        self._print(
            "[blue]# Done [green]✓[/green][/blue]"
            if shutil.which(package) else
            "[yellow]# Error [red]✗[/yellow][/red]"
        )

    def search(self, pattren: str) -> None:
        console = Console()
        bar = ProgressBar(width=shutil.get_terminal_size()[0] - 10, total=100)
        packages = re.findall(r"\n([\w\-\_\S]*)/", self._popen(f"pkg search {pattren}"))
        get_item = lambda key, data: data.get(key) if key in data else '[red]None[/red]'
        table = Table(
            title="Search for Packages",
            caption=f"{len(packages)} Packages.",
            caption_justify="right",
            expand=True,
        )
        table.add_column("Package", style="cyan", header_style="bright_cyan")
        table.add_column("Size", style="green", header_style="bright_green")
        table.add_column("Exists", style="yellow", header_style="bright_yellow")
        table.add_column("HomePage", style="blue", header_style="bright_blue")
        i = 0
        console.show_cursor(False)
        for pkg in packages:
            information = self._info_package_as_json(pkg)        
            _exists = True if shutil.which(pkg) else False
            table.add_row(
                get_item("Package", information),
                get_item("Installed-Size", information),
                (str(_exists) if _exists else f"[red]{_exists}[/red]"),
                get_item("Homepage", information),
                style="dim" if _exists else "none"
            )
            point = round(i/len(packages)*100)
            bar.update(point)
            console.print(bar)
            console.file.write(f' {point}%\r')
            i+=1
        self._print(table)
        console.show_cursor(True)
        

if __name__ == "__main__":
    argv = sys.argv[1:]
    packageshelper = PackagesHelper()
    help_msg = lambda: packageshelper._panel(base64.b64decode(DESCRIPTION).decode(), "[white]package[red]-[/red]helper", expand=False, border_style="cyan")
    if len(argv) >= 2:
        try:
            packageshelper.__getattribute__(argv[0])(argv[1])
        except AttributeError:
            help_msg()
        except Exception as e:
            print(f"# {e.__class__.__name__}: {str(e)}")
            help_msg()
    else:
        help_msg()
        
