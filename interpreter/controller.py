from os import path
from abc import ABCMeta, abstractmethod


# Subscriber
class Observer(metaclass=ABCMeta):
    def __init__(self):
        self.command = None
        self.input = None

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def set_subject(self, subject):
        pass

    @abstractmethod
    def get_command(self):
        pass

    @abstractmethod
    def get_input(self):
        pass


class Controller(Observer):
    def __init__(self, database, filehandler, graph):
        Observer.__init__(self)
        self.db_handler = database
        self.data = None
        self.filehandler = filehandler
        self.graph = graph
        self.file = None
        self.directory = path.realpath(path.curdir)
        self.subject = None

    def set_subject(self, subject):
        self.subject = subject

    def start(self):
        self.subject.cmdloop()

    def get_command(self):
        return self.subject.command

    def get_input(self):
        return self.subject.input

    def update(self):
        self.command = self.get_command()
        self.input = self.get_input()
        self.execute()

    def execute(self):
        if self.command == "cd":
            self.cd(self.input)
        elif self.command == "pwd":
            self.pwd(self.input)
        elif self.command == "load":
            self.load(self.input)
        elif self.command == "save":
            self.save(self.input)
        elif self.command == "graph":
            self.make_graph(self.input)

    def cd(self, arg):
        try:
            line = arg.lower()
            if path.isdir(path.realpath(path.relpath(path.join(self.directory, line)))):
                self.directory = path.realpath(path.relpath(path.join(self.directory, line)))
            else:
                print("Not a valid directory")
        except ValueError:
            print("No path was specified, please try again")
        print(self.directory)

    def load(self, arg):
        if arg.lower() != "database":
            self.load_file(arg)
        else:
            self.load_database()

    def load_file(self, arg):
        try:
            if path.isfile(path.realpath(path.join(self.directory, path.relpath(arg)))):
                self.file = path.realpath(path.join(self.directory, path.relpath(arg)))
                self.filehandler.load(self.file)
                self.subject.prompt = '(Interpreter: ' + path.basename(self.file) + ') '
                self.data = self.filehandler.get_process_data()
            else:
                print("Path is not a file")
        except ValueError:
            print("No path was specified, please try again")

    def load_database(self):
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

    def save(self, arg):
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

    def make_graph(self, arg):
        graph_type = arg
        filename = input("What would you like the filename to be? : ")
        self.graph.data = self.data
        criteria_select = input("Would you like to set a criteria? [Y/N] : ")
        if criteria_select.lower() == "Y":
            criteria = input("What criteria would you like to set? [key value] : ")
            criteria = criteria.split(" ")
            key = criteria[0]
            value = criteria[1]
            self.graph.set_criteria(key, value)
        x = input("What data would you like to use? [key] : ")
        y = input("What labels would you like to use? [key] : ")
        title = input("What is the title of the graph? : ")
        self.graph.set_path(path.join(self.directory, filename))
        self.graph.set_title(title)
        self.graph.set_keys(x, y)
        self.graph.draw(graph_type)

    def pwd(self, arg):
        print(self.directory)












