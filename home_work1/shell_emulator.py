import toml
from shell import Shell
from shell_gui import ShellGUI
import tkinter as tk


def main():
    config = toml.load('config.toml')['settings']

    shell = Shell(config)

    root = tk.Tk()
    gui = ShellGUI(root, shell)
    gui.run()


if __name__ == "__main__":
    main()