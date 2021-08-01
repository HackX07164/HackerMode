import os

from flask import Flask
from flask import render_template
from flask import request

from rich.console import Console
from rich import print
from rich.table import Table
import logging

os.environ['WERKZEUG_RUN_MAIN'] = 'true'
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

print("Serve running on: http://127.0.0.1:5000")
print("[ ctrl + c ] to exit")


@app.route('/', methods=['GET', 'POST'])
def index():
    table = Table()
    table.add_column("option", style="bright_cyan")
    table.add_column("value", style="green")
    if len(request.form):
        for i in request.form:
            value = str(request.form[i])
            if value.strip():
                table.add_row(str(i), value)
        console = Console()
        console.print(table)
    return render_template('index.html')


app.run()
