from interpreter.controller import Controller
from interpreter.database_handler import DatabaseHandler
from interpreter.filehandler import FileHandler
from interpreter.prompt import Prompt
from interpreter.chart import Graph


if __name__ == '__main__':
    filehandler = FileHandler()
    databasehandler = DatabaseHandler()
    graph = Graph()
    prompt = Prompt()
    controller = Controller(prompt, databasehandler, filehandler, graph)
    prompt.attach(controller)
    controller.start()


