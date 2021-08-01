import os
import re

from N4Tools.Design import ThreadAnimation
from bs4 import BeautifulSoup
from requests_html import HTMLSession


class PullSites:
    def __init__(self, url, project_name, page_name):
        self.url = url
        self.project_name = project_name
        self.page_name = page_name

    def start(self):
        self.session = HTMLSession()
        response = self.session.get(self.url)
        response.html.render()

        self.html_page = response.text
        self.html_soup = BeautifulSoup(self.html_page, "html.parser")

        self.create_project_folders()
        self.download_web_files()
        self.save_html_page(self.page_name)
        self.create_server()

    def create_project_folders(self):
        folders = (
            self.project_name,
            self.project_name + "/templates",
            self.project_name + "/static"
        )
        for folder in folders:
            try:
                os.mkdir(folder)
            except FileExistsError:
                pass

    def download_web_files(self):
        pattren = r'^(https?|\/).*?\.(jpg|png|jpeg|gif|svg|css|js|ico|xml|woff|json)+$'
        for tag in self.html_soup.open_tag_counter.keys():
            for soup in self.html_soup.find_all(tag):
                for attr in ['src', 'href', 'content']:
                    if text := soup.get(attr):
                        if url := re.search(pattren, text):
                            url = url[0]
                            if url.startswith("/"):
                                url = self.url + url
                            soup[attr] = (
                                    '{{ url_for("static", filename="%s") }}'
                                    % self.get_filename_from_url(url)
                            )
                            self.download_file(url)

    def get_filename_from_url(self, url):
        return url.split("/")[-1]

    @ThreadAnimation()
    def download_file(thread, self, url):
        file_path: str = f"{self.project_name}/static/{self.get_filename_from_url(url)}"
        if not os.path.exists(file_path):
            file_data: bytes = self.session.get(url).content
            with open(file_path, "wb") as file:
                file.write(file_data)
            thread.kill()
            print("[+]Downloaded..", file_path)

    def save_html_page(self, page_name):
        page: str = self.html_soup.prettify()
        with open(f"{self.project_name}/templates/{page_name.split('/')[-1]}.html", "w") as html_file:
            html_file.write(page)

    def create_server(self):
        server_path = f"{self.project_name}/__main__.py"
        if os.path.exists(server_path):
            with open(server_path, 'r') as file:
                server_text_file = file.read()
        else:
            with open(os.path.abspath(__file__).rsplit("/", 1)[0] + "/flask_app.py", 'r') as file:
                server_text_file = file.read()

        pattern = r'''(\@\w+\.route\(["']([\w\/]+)["'].*?\)\s+def \w+\(.*\):\s(?:[ \t]+.+\n){1,}\s+return render_template\(['"](.+)['"]\))'''
        page_functions = re.findall(pattern, server_text_file)
        pages = []
        for function in page_functions:
            function_body, page_route, page_file = function
            pages.append(page_route)

        if (page_name := '/' + self.page_name.replace('index', '')) not in pages:
            new_page = function_body + self.page_function(page_name)
            server_text_file = server_text_file.replace(
                function_body, new_page
            )
            pages.append(page_name)

        with open(f"{self.project_name}/__main__.py", "w") as file:
            file.write(server_text_file)

        print(f"\033[0;33mPAGES:", *pages, sep='\n  \033[0m')
        print(f"\n# DONE ✅")

    def page_function(self, page_name):
        return f'''

@app.route('{page_name}', methods=['GET', 'POST'])
def {page_name[1:].split("/")[-1]}():
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
    return render_template('{page_name[1:].split("/")[-1]}.html')'''
