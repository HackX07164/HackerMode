# coding: utf-8
import os
import sys

HACKERMODE_FOLDER_NAME = "HackerMode"


class Variables:
    @property
    def BASHRIC_FILE_PATH(self) -> str:
        if (shell := os.environ.get('SHELL')):
            if shell.endswith("bash"):
                path = os.path.join(shell.split("/bin/")[0], "etc/bash.bashrc")
                if not os.path.exists(path):
                    path = "/etc/bash.bashrc"
            elif shell.endswith("zsh"):
                path = os.path.join(shell.split("/bin/")[0], "etc/zsh/zshrc")
                if not os.path.exists(path):
                    path = "/etc/zsh/zshrc"
        return path

    @property
    def HACKERMODE_SHORTCUT(self) -> str:
        """HackerMode shortcut"""
        return f"\nalias HackerMode='source {self.HACKERMODE_ACTIVATE_FILE_PATH}'"

    @property
    def HACKERMODE_ACTIVATE_FILE_PATH(self) -> str:
        """To get HackerMode activate file"""
        return os.path.join(self.HACKERMODE_INSTALL_PATH, "HackerMode/bin/activate")

    @property
    def HACKERMODE_PATH(self) -> str:
        """To get real HackerMode path"""
        return '/'.join(os.path.abspath(__file__).split('/')[:-2])

    @property
    def HACKERMODE_BIN_PATH(self) -> str:
        """To get HackerMode [HackerMode/bin/] directory"""
        return os.path.join(self.HACKERMODE_PATH, "bin")

    @property
    def HACKERMODE_TOOLS_PATH(self) -> str:
        """To get the HackerMode [HackerMode/tools/] path"""
        return os.path.join(self.HACKERMODE_PATH, "tools")

    @property
    def HACKERMODE_INSTALL_PATH(self) -> str:
        """To get the install path [~/.HackerMode/]"""
        ToolPath = os.path.join(os.environ['HOME'], '.HackerMode')
        if not os.path.isdir(ToolPath):
            os.mkdir(ToolPath)
        return ToolPath

    @property
    def PLATFORME(self) -> str:
        """To get the platform name"""
        if sys.platform in ('win32', 'cygwin'):
            return 'win'

        elif sys.platform == 'darwin':
            return 'macosx'

        elif 'PWD' in os.environ and 'com.termux' in os.environ['PWD']:
            return 'termux'

        elif sys.platform.startswith('linux') or sys.platform.startswith('freebsd'):
            return 'linux'
        return 'unknown'


Variables = Variables()

if __name__ == "__main__":
    print(eval(f"Variables.{sys.argv[1]}"))
