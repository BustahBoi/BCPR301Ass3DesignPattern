from cmd import Cmd
# from interpreter.chart import Graph
# from os import path
from abc import ABCMeta, abstractmethod


# Publisher
class Subject(metaclass=ABCMeta):
    def __init__(self):
        self.subscribers = list()
        self.command = False
        self.input = None

    def attach(self, observer):
        self.subscribers.append(observer)

    def detach(self, observer):
        self.subscribers.remove(observer)

    def notify(self):
        for sub in self.subscribers:
            sub.update()

    def set_state(self, command, arg):
        self.command = command
        self.input = arg
        self.notify()

    def get_command(self):
        return self.command

    def get_input(self):
        return self.input


class Prompt(Cmd, Subject):

    def __init__(self):
        Cmd.__init__(self)
        Subject.__init__(self)
        self.intro = "Welcome to our custom Interpreter shell. Type help or ? to list commands.\n"
        self.prompt = '(Interpreter) '

    def do_cd(self, arg):
        self.set_state("cd", arg)

    def do_load(self, arg):
        self.set_state("load", arg)

    def do_graph(self, arg):
        self.set_state("graph", arg)

    def do_exit(self, arg):
        print("Exiting ......")
        return True

    def do_pwd(self, arg):
        self.set_state("pwd", arg)

    def do_save(self, arg):
        self.set_state("save", arg)

