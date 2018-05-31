from cmd import Cmd
from interpreter.database_handler import DatabaseHandler
from interpreter.filehandler import FileHandler
from interpreter.chart import Graph
from os import path


class Shell(Cmd):

    def __init__(self):
        super().__init__()
        self.db_handler = DatabaseHandler()
        self.data = None
        self.filehandler = FileHandler()
        self.graph = None
        self.intro = "Welcome to our custom Interpreter shell. Type help or ? to list commands.\n"
        self.prompt = '(Interpreter) '
        self.file = None
        self.directory = path.realpath(path.curdir)

    # Wesley
    def do_cd(self, arg):
        """
        Syntax:
            cd [path]
            relative traversal through file structure, same as windows

        :param arg:
            path: [string]

        :return:
            New working directory
        """
        try:
            line = arg.lower()
            start_path = path.realpath(path.relpath(line))
            if self.directory is None and path.isdir(start_path):
                self.directory = start_path # pragma: no cover
                print(self.directory) # pragma: no cover
            elif path.isdir(path.realpath(path.relpath(path.join(self.directory, line)))):
                self.directory = path.realpath(path.relpath(path.join(self.directory, line)))
                print(self.directory)
                # print("else")
            else:
                print("Not a valid directory")
        except ValueError:
            print("No path was specified, please try again")
        except TypeError:    # pragma: no cover
            print("Type of none is invalid")  # pragma: no cover

    def do_load(self, arg):
        """
        Syntax:
            load [filename] or [database]

        :param arg:
            filename: [string]

        :return:
            File has been set
        """
        if arg.lower() != "database":
            try:
                if path.isfile(path.realpath(path.join(self.directory, path.relpath(arg)))):
                    self.file = path.realpath(path.join(self.directory, path.relpath(arg)))
                    self.filehandler.load(self.file)
                    self.prompt = '(Interpreter: ' + path.basename(self.file) + ') '
                    self.data = self.filehandler.read()
                else:
                    print("Path is not a file")
            except ValueError:
                print("No path was specified, please try again")
        elif arg.lower() == "database":
            db = input("remote or local?")
            try:
                if db.lower() == "local":
                    db_name = input("What is the name of the database? >")
                    self.db_handler.set_local(db_name)
                    self.db_handler.insert_local_dict(self.data)
                    self.db_handler.get_local()
                    if self.data:
                        print("Data has been loaded")
                    else:
                        print("No data was found")
                elif db.lower() == "remote":
                    host = input("What is the hostname? >")
                    user = input("What is the username? >")
                    password = input("Input a password >")
                    db = input("What is the database name? >")
                    self.db_handler.set_remote(host=host, user=user, password=password, db=db)
                    self.db_handler.insert_remote_dict(self.data)
                    self.data = self.db_handler.get_remote()
                    if self.data:
                        print("Data has been loaded")
                    else:
                        print("No data was found")
                else:
                    print("invalid database type")
            except ValueError:
                print("Try again...")
            except AttributeError:
                print("No data found")
        else:
            print("Invalid command")

    def do_graph(self, arg):
        """
        Syntax:
            graph [graphtype] [filename]
            Displays a graph of the loaded data

        :param arg:
            graphtype: [-bar | -scatter | -pie]
            filename: [string]

        :return:
            The graph
        """
        commands = arg.split(" ")
        if self.data:
            try:
                if commands[0] == "pie" or commands[0] == "scatter" or commands[0] == "bar":
                    a_path = path.join(self.directory, commands[1] + ".html")
                    self.graph = Graph()
                    self.graph.set_data(self.data, commands[0], a_path)
                    criteria = input("What are the criteria? ([key] [value - optional]) > ")
                    crit = criteria.split(" ")
                    print("_______________")
                    print(criteria)
                    if len(crit) > 1:
                        self.graph.set_criteria(crit[0], crit[1])
                    else:
                        self.graph.set_criteria(crit[0])
                    keys = input("What keys to use? ([key1] [key2]) > ")
                    a_key = keys.split(" ")
                    if len(a_key) > 1:
                        self.graph.set_keys(a_key[0], a_key[1])
                    else:
                        self.graph.set_keys(a_key[0])
                    title = input("What is the title? >")
                    if len(a_key) > 1:
                        self.graph.draw(a_key[0], a_key[1], title)
                    else:
                        self.graph.draw(a_key[0], a_key[0], title)
                else:
                    print("filename is invalid")
            except IndexError:
                # print(criteria)
                print("You have entered invalid criteria")
            except KeyError:
                print("This key is invalid")
        else:
            print("Please set data before attempting to create a graph")

    def do_quit(self, arg):
        """
        Syntax:
            quit
            Quit from my CMD

        :param arg:
            none

        :return:
            True
        """
        print("Quitting ......")
        return True

    # Sam
    def do_pwd(self, arg):
        """
        Syntax:
            pwd
            Print the current working directory

        :param arg:
            none

        :return:
            The current working directory
        """
        print(path.split(self.directory)[0])

    # James
    def do_save(self, arg):
        """
        Syntax: save [database]
        :param arg:
        :return:
        """
        commands = arg.split(" ")
        if self.data:
            try:
                if commands[0].lower() == "local":
                    db_name = input("What would you like to name the database? >")
                    self.db_handler.set_local(db_name)
                    self.db_handler.insert_local_dict(self.data)
                elif commands[0].lower() == "remote":
                    host = input("What is the hostname? >")
                    user = input("What is the username? >")
                    password = input("Input a password >")
                    db = input("What is the database name? >")
                    self.db_handler.set_remote(host, user, password, db)
                    self.db_handler.insert_remote_dict(self.data)
                else:
                    print("invalid database type")
            except ValueError:
                print("Try again...")
        else:
            print("Please load data before attempting to save")


if __name__ == '__main__':
    Shell().cmdloop()
