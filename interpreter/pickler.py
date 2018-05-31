from pickle import dumps
from pickle import Unpickler as Unpick
from io import BytesIO


class Pickler:

    @staticmethod
    def pickle_dictionary_values(dictionary):
        """
        Will take a dictionary containing dictionary values and return a dictionary with pickled values, keys are
        maintained
        :param dictionary:
        :return: dictionary{{key: value(pickled)}}
        >>>Pickler.pickle_dictionary_values({1: {"asdfdsafdsaf"}})
        """
        pickled_dict = dict()
        for key, value in dictionary.items():
            pickled_dict[key] = dumps(value)
        return pickled_dict

    @staticmethod
    def unpickle_dictionary(the_list):
        """Input a dictionary with key value
            where value is pickled and return a dictionary
            with unpickled values"""
        unpickled_dict = dict()
        for record in the_list:
            file = BytesIO(record[1])
            unpickled_dict[record[0]] = Unpick(file).load()
        return unpickled_dict





