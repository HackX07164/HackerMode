import os
import json
import shutil

from lib.config import Config
from lib.variables import (
    Variables,
    HACKERMODE_FOLDER_NAME,
)

with open(os.path.join(Variables.HACKERMODE_PATH, 'packages.json')) as fp:
    PACKAGES = json.load(fp)["PACKAGES"]

BASE_PYHTON_MODULES = (
    'requests',
    'rich',
    'N4Tools==1.7.1',
    'bs4',
    'pyfiglet',
    'arabic_reshaper',
    'python-bidi',
)

BASE_PACKAGES = (
    'git',
    'pip3',
)

RED = '\033[1;31m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
NORMAL = '\033[0m'
UNDERLINE = '\033[4m'
BOLD = '\033[1m'


class Installer:
    installed_successfully = {
        'base': []
    }

    def installed_msg(self, package, message=False):
        default_message = f'{package.split("=")[0]} installed successfully.'
        return f'{NORMAL}({GREEN}✔{NORMAL}) {GREEN}{default_message if not message else message}'

    def not_installed_msg(self, package, message=False, is_base=False):
        default_message = f'not able to install "{package}".{NORMAL}'
        color = RED if is_base else YELLOW
        return f'{NORMAL}({color}{"✗" if is_base else "!"}{NORMAL}) {color}{default_message if not message else message}'

    def installer(self):
        '''Install all HackerMode packages and modules'''

        # Install the basics packages:
        for PACKAGE_NAME, SETUP in PACKAGES.items():
            for COMMANDS in SETUP[Variables.PLATFORME]:
                os.system(COMMANDS)

        # Install the basics python3 modules:
        MODULES = os.path.join(Variables.HACKERMODE_PATH, 'requirements.txt')
        if Variables.PLATFORME == 'linux':
            os.system(f'sudo pip3 install -r {MODULES}')
        elif Variables.PLATFORME == 'termux':
            os.system(f'pip install -r {MODULES}')

        # Install tools packages:
        if Config.get('actions', 'DEBUG', default=False):
            print('# In debug mode can"t run setup')
            return

        old_path = os.getcwd()
        try:
            for root, tools, files in os.walk(Variables.HACKERMODE_TOOLS_PATH):
                for tool in tools:
                    if os.path.exists(os.path.join(Variables.HACKERMODE_TOOLS_PATH, tool)):
                        os.chdir(os.path.join(Variables.HACKERMODE_TOOLS_PATH, tool))
                        if os.path.isfile("setup"):
                            if Variables.PLATFORME == 'linux':
                                os.system(f'sudo chmod +x setup')
                            elif Variables.PLATFORME == 'termux':
                                os.system(f'chmod +x setup')
                            os.system("./setup")
                        else:
                            print(f"{YELLOW}# no setup file in '{tool}'!")
                    else:
                        print("# Not find", os.path.join(Variables.HACKERMODE_TOOLS_PATH, tool))
                break
        finally:
            os.chdir(old_path)

    def install(self):
        # check platform...
        if not Variables.PLATFORME in ('termux', 'linux'):
            if Variables.PLATFORME == 'unknown':
                print("# The tool could not recognize the system!")
                print("# Do You want to continue anyway?")
                while True:
                    if input('# [Y/N]: ').lower() == 'y':
                        break
                    else:
                        print('# good bye :D')
                        return
            else:
                print(f"# The tool does not support {Variables.PLATFORME}")
                print('# good bye :D')
                return

        # install packages
        self.installer()

        # check:
        print('\n# CHRCKING:')
        self.check()

        if Variables.PLATFORME == "termux":
            try:
                os.listdir("/sdcard")
            except PermissionError:
                os.system("termux-setup-storage")

        if Config.get('actions', 'IS_INSTALLED', cast=bool, default=False):
            return

        # Move the tool to "System.TOOL_PATH"
        if not all(self.installed_successfully['base']):
            print(f'# {RED}Error:{NORMAL} some of the basics package not installed!')
            return

        if Config.get('actions', 'DEBUG', cast=bool, default=True):
            print('# In DEBUG mode can"t move the tool\n# to "System.TOOL_PATH"!')
            return

        if os.path.isdir(HACKERMODE_FOLDER_NAME):
            try:
                shutil.move(HACKERMODE_FOLDER_NAME, Variables.HACKERMODE_INSTALL_PATH)
                print(f'# {GREEN}HackerMode installed successfully...{NORMAL}')
                Config.set('actions', 'IS_INSTALLED', True)
            except shutil.Error as e:
                self.delete()
                print(e)
                print('# installed failed!')
        else:
            self.delete()
            print(f'{RED}# Error: the tool path not found!')
            print(f'# try to run tool using\n# {GREEN}"python3 HackerMode install"{NORMAL}')
            print('# installed failed!')

    def check(self):
        '''To check if the packages has been
        installed successfully.
        '''
        with open(os.path.join(Variables.HACKERMODE_PATH, "requirements.txt"), "r") as f:
            PYHTON_MODULES = f.read().split("\n")
        PYHTON_MODULES_INSTALLED = os.popen("pip3 freeze").read().split("\n")

        # check packages:
        for package in PACKAGES.keys():
            if not PACKAGES[package][Variables.PLATFORME]:
                continue
            if os.path.exists(os.popen(f"which {package.strip()}").read().strip()):
                print(self.installed_msg(package))
                if package in BASE_PACKAGES:
                    self.installed_successfully['base'].append(True)
            else:
                print(self.not_installed_msg(package, is_base=(package in BASE_PACKAGES)))
                if package in BASE_PACKAGES:
                    self.installed_successfully['base'].append(False)

        # check python modules:
        for module in PYHTON_MODULES:
            if module.strip() in PYHTON_MODULES_INSTALLED:
                print(self.installed_msg(module))
                if module in BASE_PYHTON_MODULES:
                    self.installed_successfully['base'].append(True)

            else:
                try:
                    exec(f"import {module.split('=')[0].strip()}")
                    print(self.installed_msg(module))
                    if module in BASE_PYHTON_MODULES:
                        self.installed_successfully['base'].append(True)
                except ImportError:
                    print(self.not_installed_msg(module, is_base=(module in BASE_PYHTON_MODULES)))
                    if module in BASE_PYHTON_MODULES:
                        self.installed_successfully['base'].append(False)

    def update(self):
        if not Config.get('actions', 'DEBUG', cast=bool, default=False):
            os.system(
                f'cd {Variables.HACKERMODE_PATH} && rm -rif {HACKERMODE_FOLDER_NAME} && git clone https://github.com/Arab-developers/{HACKERMODE_FOLDER_NAME}')
            self.installer()
        else:
            print("# can't update in the DEUBG mode!")

    def delete(self):
        bin_path = os.path.join(os.environ["SHELL"].split("/bin/")[0], "/bin/HackerMode")
        tool_path = os.path.join(os.environ["HOME"], ".HackerMode")
        if os.path.exists(bin_path):
            os.remove(bin_path)
        if os.path.exists(tool_path):
            shutil.rmtree(tool_path)
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
            if data.find(Variables.HACKERMODE_SHORTCUT.strip()) != -1:
                with open(path, "w") as f:
                    f.write(data.replace(Variables.HACKERMODE_SHORTCUT.strip(), ""))
        print("# The deletion was successful...")


Installer = Installer()

if __name__ == '__main__':
    print('# To install write "python3 -B HackerMode install"')
