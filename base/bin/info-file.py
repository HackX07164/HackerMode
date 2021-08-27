#!/usr/bin/python
import re
import os
import sys
import time
import base64

from rich import box
from rich.table import Table
from rich.panel import Panel
from rich.filesize import decimal
from rich.console import Console
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    ProgressColumn,
    SpinnerColumn
)

class FileSizeColumn(ProgressColumn):

    def render(self, task) -> str:
        return f"[cyan]{decimal(task.completed)}"


class ParserFile:
    def parser_model(self, name: str) -> str:
        pattrens = {
            "[green]python": "\.(?:py|pyc)$",
            "[spring_green2]c++": "\.(?:cc|cpp|cxx|c|c\+\+|h|hpp|hh|hxx|\+\+h|h)$",
            "[blue]java": "\.(?:java|class)$",
            "[sandy_brown]progreming more": "\.(?:html|css|js|javascript|xml|dart|exe|json|bash|sh)$",
            "[yellow]application": "\.(?:apk|exe)$",
            "[steel_blue1]image": "\.(?:jpg|png|jpeg|gif|svg|ico)$",
            "[green]️video": "\.(?:mp4|mkv)$",
            "[magenta2]audio": "\.(?:mp3)$",
            "[steel_blue]more": "."
        }
        for model, pattren in pattrens.items():
            if re.findall(pattren, name):
                return model

    def parser_size(self, path) -> tuple:
        sizes = {}
        Max = 0
        for p, dirs, files in os.walk(path):
            for file in files:
                model = self.parser_model(file)
                try:
                    size = os.path.getsize(os.path.join(p, file))
                except FileNotFoundError:
                    continue
                Max += size
                if model in sizes:
                    sizes[model].append(size)
                else:
                    sizes[model] = [size]
        return (sizes, Max)
        
    @staticmethod
    def parser_sorted_file_by_size(path: str) -> dict:
        data = {}
        for p, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(p, file)
                try:
                    size = os.path.getsize(file_path)
                    if size == 0:
                        continue
                except FileNotFoundError:
                    continue
                if size in data:
                    data[size].append(file_path)
                else:
                    data[size] = [file_path]
        return data

    @staticmethod
    def read(path: str) -> bytes:
        with open(path, "rb") as f:
            return f.read()

class Specialist:
    def __init__(self, path: str) -> None:
        with Progress(
            TextColumn("[progress.desciption]{task.description}"),
            SpinnerColumn(spinner_name="point"),
            BarColumn(),
            transient=True,
        ) as progress:
            progress.add_task("[green]Starting ", start=False)
            self.sizes, self.Max = ParserFile().parser_size(path)
        
    def start(self, sleep: int=0.00001) -> None:
        with Progress(
            SpinnerColumn(spinner_name="dots9", finished_text="[blue]✓"),
            TextColumn("[progress.desciption]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            FileSizeColumn()
        ) as progress:
            tasks = {
                k: progress.add_task(f"{k}", total=self.Max)
                for k, v in sorted(self.sizes.items())
            }
            
            progress.add_task("[cyan]ALL", total=self.Max)
            while list(self.sizes.values()) != [[]]*len(self.sizes):
                for k, v in self.sizes.items():
                    for a in v:
                        progress.advance(tasks[k], a)
                        progress.advance(len(tasks), a)
                        self.sizes[k] = self.sizes[k][1:] # pop first
                        break
                    time.sleep(sleep)

class RepeaterFiles:
    def __init__(self, path: str) -> None:
        self.data = ParserFile.parser_sorted_file_by_size(path)


    def start(self) -> Table:
        with Progress(
            TextColumn("[progress.desciption]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            transient=True,
        ) as progress:
            progress.add_task("[green]Starting ", total=len(self.data))
            repeater, size_repeater = 0, 0
            read = ParserFile.read
            table = Table(
                title="Repeater files",
                box=box.ROUNDED,
                expand=False,
            )
            table.add_column("path", style="cyan", header_style="bright_cyan")
            table.add_column("size", style="blue", header_style="bright_blue")
            table.add_column("model", style="yellow", header_style="bright_yellow")
            for size, paths in sorted(self.data.items()):
                paths = sorted(paths)
                #print(paths[0])
                original = read(paths[0])
                row = []
                for path in paths[1:]:
                 #   print(path)
                    if read(path) == original:
                        row.append((path, decimal(size), "repeater"))
                        size_repeater += size
                    
                if row:
                    table.add_row(paths[0], decimal(size), "original")
                    list(map(lambda args: table.add_row(*args, style="dim"), row))
                    repeater += len(row)
                # remove size CPU
                del original
                del row
                del paths
                progress.advance(0, 1)
            table.caption = f"The number of duplicate files is equal [blue]{repeater}[/blue] and size is [blue]{decimal(size_repeater)}[/blue]"
        Console().print(
            table
        )
            
                
class InfoFile:
    @staticmethod
    def specialist(path: str) -> None:
        Specialist(path).start()

    @staticmethod
    def repeater(path: str) -> None:
        RepeaterFiles(path).start()

    @staticmethod
    def help_massage() -> None:
        Console().print(
            Panel(
                base64.b64decode(b'ewogICAgW2JsdWVdZnJvbVsvYmx1ZV1bcmVkXTpbL3JlZF0gW2N5YW5dQHBzaF90ZWFtWy9jeWFuXVtyZWRdLlsvcmVkXVt5ZWxsb3ddSGFja2VyTW9kZVsveWVsbG93XSwKICAgIFtibHVlXWV4YW1wbGVbcmVkXTpbL3JlZF0KICAgICAgICBbcmVkXSQgW29yY2hpZDJdaW5mb1svb3JjaGlkMl0tW29yY2hpZDJdZmlsZVsvb3JjaGlkMl1bL3JlZF0gW2N5YW5dc3BlY2lhbGlzdFsvY3lhbl0gW3llbGxvd11wYXRoL3RvL215ZGlyL1sveWVsbG93XQogICAgICAgIFtyZWRdJCBbb3JjaGlkMl1pbmZvWy9vcmNoaWQyXS1bb3JjaGlkMl1maWxlWy9vcmNoaWQyXVsvcmVkXSBbY3lhbl1zcGVjaWFsaXN0Wy9jeWFuXSBbeWVsbG93XS9zZGNhcmQvWy95ZWxsb3ddCiAgICAgICAgW3JlZF0kIFtvcmNoaWQyXWluZm9bL29yY2hpZDJdLVtvcmNoaWQyXWZpbGVbL29yY2hpZDJdWy9yZWRdIFtjeWFuXXJlcGVhdGVyWy9jeWFuXSBbeWVsbG93XXBhdGgvdG8vbXlkaXIvWy95ZWxsb3ddCiAgICAgICAgW3JlZF0kIFtvcmNoaWQyXWluZm9bL29yY2hpZDJdLVtvcmNoaWQyXWZpbGVbL29yY2hpZDJdWy9yZWRdIFtjeWFuXXJlcGVhdGVyWy9jeWFuXSBbeWVsbG93XS9zZGNhcmQvWy95ZWxsb3ddCiAgICBzcGVjaWFsaXN0Wy9ibHVlXVtyZWRdOlsvcmVkXSBTcGVjaWFsaXN0IGFsbCBmaWxlcywKICAgIFtibHVlXXJlcGVhdGVyWy9ibHVlXVtyZWRdOlsvcmVkXSBmaW5kIGFuZCBnZXQgYWxsIGZpbGUgcmVwZWF0ZXIsCn0=').decode(),
                title="[white]info[red]-[/red]file[/white]",
                expand=False,
                border_style="cyan",
            )
        ); exit()

if __name__ == "__main__":
    argv = sys.argv[1:]
    if len(argv) >= 2:
        try:
            eval(f'InfoFile.{argv[0]}')(argv[1])
        except Exception:
            InfoFile.help_massage()
    else:
        InfoFile.help_massage()
    
