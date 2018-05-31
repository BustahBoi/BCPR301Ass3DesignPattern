from plotly import offline
from plotly.graph_objs import Scatter, Layout, Pie, Bar
from abc import ABCMeta, abstractmethod


class GraphDirector:
    def __init__(self, builder):
        self.graph_builder = builder

    def build_graph(self):
        self.graph_builder.set_layout()
        self.graph_builder.set_x()
        self.graph_builder.set_y()
        self.graph_builder.set_data()


class GraphBuilder(metaclass=ABCMeta):
    def __init__(self, path, data, x, y, title):
        self.data = data
        self.graph = dict()
        self.title = title
        self.path = path
        self.x = x
        self.y = y

    @abstractmethod
    def set_x(self):
        pass

    @abstractmethod
    def set_y(self):
        pass

    @abstractmethod
    def set_data(self):
        pass

    @abstractmethod
    def set_layout(self):
        pass


class PieGraph(GraphBuilder):

    def set_layout(self):
        self.graph["layout"] = Layout(title=self.title)

    def set_x(self):
        self.graph["x"] = self.data["x"][self.x]

    def set_y(self):
        self.graph["y"] = self.data["y"][self.y]

    def set_data(self):
        self.graph["data"] = [Pie(labels=self.graph["y"], values=self.graph["x"])]

    def draw(self):
        offline.plot({"data": self.graph["data"], "layout": self.graph["layout"]}, filename=self.path)


class BarGraph(GraphBuilder):

    def set_layout(self):
        self.graph["layout"] = Layout(title=self.title)

    def set_x(self):
        self.graph["x"] = self.data["x"][self.x]

    def set_y(self):
        self.graph["y"] = self.data["y"][self.y]

    def set_data(self):
        self.graph["data"] = [Bar(x=self.data["x"], y=self.data["y"])]

    def draw(self):
        offline.plot({"data": self.graph["data"], "layout": self.graph["layout"]}, filename=self.path)


class ScatterGraph(GraphBuilder):

    def set_layout(self):
        self.graph["layout"] = Layout(title=self.title)

    def set_x(self):
        self.graph["x"] = self.data["x"][self.x]

    def set_y(self):
        self.graph["y"] = self.data["y"][self.y]

    def set_data(self):
        self.graph["data"] = [Scatter(y=self.data["y"], x=self.data["x"])]

    def draw(self):
        offline.plot({"data": self.graph["data"], "layout": self.graph["layout"]}, filename=self.path)


class Graph:
    def __init__(self):
        self.__data = None
        self.__path = None
        self.__x = None
        self.__y = None
        self.__title = None

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    def set_criteria(self, key, value):
        self.data = {record[0]: record[1] for record in self.data.items() if record[1][key] == value}

    def set_keys(self, x, y):
        keys_a = list()
        keys_b = list()
        self.__y = y
        self.__x = x
        for (key, value) in self.data.items():  # row
            for (key1, value1) in value.items():  # key value
                if key1.lower() == y:
                    keys_a.append(value1)
                if key1.lower() == x:
                    keys_b.append(value1)
        self.data = {"y": {self.__y: keys_a}, "x": {self.__x: keys_b}}

    def set_path(self, path):
        self.__path = path

    def set_title(self, title):
        self.__title = title

    def draw(self, arg):
        if arg == "pie":
            piebuilder = PieGraph(self.__path, self.__data, self.__x, self.__y, self.__title)
            director = GraphDirector(piebuilder)
            director.build_graph()
            piebuilder.draw()
        elif arg == "bar":
            barbuilder = BarGraph(self.__path, self.__data, self.__x, self.__y, self.__title)
            director = GraphDirector(barbuilder)
            director.build_graph()
            barbuilder.draw()
        elif arg == "scatter":
            scatterbuilder = ScatterGraph(self.__path, self.__data, self.__x, self.__y, self.__title)
            director = GraphDirector(scatterbuilder)
            director.build_graph()
            scatterbuilder.draw()
        else:
            print("not a thing yo")

