import os
import json
import shutil

from lib.config import Config
from lib.variables import (
    Variables,
    HACERMODE_FOLDER_NAME,
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


class Installer:
    InstalledSuccessfully = {
        'base': []
    }

    def InstalledMsg(self, package, message=False):
        DefaultMessage = f'{package} installed successfully.'
        return f'{NORMAL}[  {GREEN}OK{NORMAL}  ] {DefaultMessage if not message else message}'

    def NotInstalledMsg(self, package, message=False, is_base=False):
        DefaultMessage = f' not able to install "{package}".'
        return f'{NORMAL}[ {RED if is_base else YELLOW}{"error" if is_base else "warning"}{NORMAL} ] {DefaultMessage if not message else message}'

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
            for tool in os.listdir(Variables.HACKERMODE_TOOLS_PATH):
                os.chdir(os.path.join(Variables.HACKERMODE_TOOLS_PATH, tool))
                if os.path.isfile("setup"):
                    if Variables.PLATFORME == 'linux':
                        os.system(f'sudo chmod +x setup')
                    elif Variables.PLATFORME == 'termux':
                        os.system(f'chmod +x setup')
                    os.system("./setup")
                else:
                    print(f"{YELLOW}# no setup file in '{tool}'!")
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
        print('\n# checking:')
        self.check()

        if Variables.PLATFORME == "termux":
            try:
                os.listdir("/sdcard")
            except PermissionError:
                os.system("termux-setup-storage")

        if Config.get('actions', 'IS_INSTALLED', cast=bool, default=False):
            return

        # Move the tool to "System.TOOL_PATH"
        if not all(self.InstalledSuccessfully['base']):
            print(f'# {RED}Error:{NORMAL} some of the basics package not installed!')
            return

        if Config.get('actions', 'DEBUG', cast=bool, default=True):
            print('# In DEBUG mode can"t move the tool\n# to "System.TOOL_PATH"!')
            return

        if os.path.isdir(HACERMODE_FOLDER_NAME):
            # add HackerMode short cut...
            if (shell := os.environ.get('SHELL')):
                if shell.endswith("bash"):
                    path = os.path.join(shell.split("/usr/")[0], "/etc/bash.bashrc")
                elif shell.endswith("zsh"):
                    path = os.path.join(shell.split("/usr/")[0], "/etc/zsh/zshrc")
                with open(path, "a") as f:
                    f.write(f"alias HackerMode='source {Variables.HACKERMODE_ACTIVATE_FILE_PATH}'")
            Config.set('actions', 'IS_INSTALLED', True)
            try:
                shutil.move(HACERMODE_FOLDER_NAME, Variables.HACKERMODE_INSTALL_PATH)
                print(f'# {GREEN}HackerMode installed successfully...{NORMAL}')
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

        # check packages:
        for package in PACKAGES.keys():
            if not PACKAGES[package][Variables.PLATFORME]:
                continue
            if os.path.exists(os.popen(f"which {package.strip()}").read()):
                print(self.InstalledMsg(package))
                if package in BASE_PACKAGES:
                    self.InstalledSuccessfully['base'].append(True)
            else:
                print(self.NotInstalledMsg(package, is_base=(package in BASE_PACKAGES)))
                if package in BASE_PACKAGES:
                    self.InstalledSuccessfully['base'].append(False)

        # check python modules:
        with open(os.path.join(Variables.HACKERMODE_PATH, "requirements.txt"), "r") as f:
            PYHTON_MODULES = f.read().split("\n")
        for module in PYHTON_MODULES:
            if module.strip() in os.popen("pip3 freeze").read().split("\n"):
                print(self.InstalledMsg(module))
                if module in BASE_PYHTON_MODULES:
                    self.InstalledSuccessfully['base'].append(True)

            else:
                print(self.NotInstalledMsg(module, is_base=(module in BASE_PYHTON_MODULES)))
                if module in BASE_PYHTON_MODULES:
                    self.InstalledSuccessfully['base'].append(False)

    def update(self):
        if not Config.get('actions', 'DEBUG', cast=bool, default=False):
            os.system(
                f'cd {Variables.HACKERMODE_PATH} && rm -rif {HACERMODE_FOLDER_NAME} && git clone https://github.com/Arab-developers/{HACERMODE_FOLDER_NAME}')
            self.installer()
        else:
            print("# can't update in the DEUBG mode!")

    def delete(self):
        root_path = os.path.join(os.environ["SHELL"].split("/bin/")[0], "/bin/sudo")
        bin_path = os.path.join(os.environ["SHELL"].split("/bin/")[0], "/bin/HackerMode")
        tool_path = os.path.join(os.environ["HOME"], ".HackerMode")
        root = ""
        if os.path.exists(root_path):
            root = "sudo"
        if os.path.exists(bin_path):
            os.remove(bin_path)
        if os.path.exists(tool_path):
            shutil.rmtree(tool_path)

        if not os.path.exists(tool_path) and not os.path.exists(bin_path):
            print("# The deletion was successful...")
        else:
            print("# Error: could not delete the tool!")


Installer = Installer()

if __name__ == '__main__':
    # tests:
    print('# To install write "python3 HackerMode install"')
