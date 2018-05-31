from abc import ABCMeta, abstractmethod


# Wesley
class DatabaseAbstract(metaclass=ABCMeta):
    # Wesley
    def __init__(self):
        self.connection = None
        self.cursor = None

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def create_table(self):
        pass

    def drop_table(self):
        """Used for testing, will drop table to clear data"""
        self.cursor.execute("Drop table if exists employee")

    def insert_dictionary(self, dictionary):
        """Write a dictionary with key and pickled values
            into the database"""
        for key, value in dictionary.items():
            self.insert_record(value)

    def get_db(self):
        """Return the database"""
        self.cursor.execute("select empNo, personal from employee")
        return self.cursor.fetchall()

    def commit(self):
        """Changes to the database need to be committed to the database"""
        self.connection.commit()

    def close(self):
        """Close the connection after each crud operation with database"""
        self.connection.close()

    @abstractmethod
    def insert_record(self, value):
        pass

    @abstractmethod
    def delete_record(self, key):
        pass

    @abstractmethod
    def update_record(self, key, value):
        pass

