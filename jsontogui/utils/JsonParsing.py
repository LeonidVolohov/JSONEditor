"""This module does basic operations to prepare input json file for further analysis.

    Typical usage example:
    ----------------------

    json_parsing = Utils()
    json_parsing.get_json_from_file("example.json")
    json_parsing.write_json_to_file("example.json")
    json_parsing.get_name_from_dict({"name": "username"})
"""
import os
import json
import gettext
from collections import OrderedDict
from configparser import ConfigParser

from utils.Utils import Utils


CONFIG_OBJECT = ConfigParser()
CONFIG_OBJECT.read(Utils().get_abs_file_path("utils/config/config.ini"))

TRANSLATE_JSONPARSING = gettext.translation(
    domain="JsonParsing",
    localedir=Utils().get_abs_file_path("utils/locale"),
    languages=[CONFIG_OBJECT.get("Language", "default_gui_language")])
TRANSLATE_JSONPARSING.install()

class JsonParsing():
    """Class parsing JSON-file for further analysis.

    Methods:
    --------
    get_json_from_file() -> dict:
        Return JSON data from given file_name
    write_json_to_file(json_data: str) -> None:
        Write to given file_name given json_data
    get_name_from_dict(data: dict) -> str
        Return str with some parameters which was found from given data
    translate(input_string: str, language: str) -> str:
        Return translated input_string from translate.py dictionary
    """

    def __init__(self) -> None:
        """Constructs all the necessary attributes for the Utils object."""
        pass

    def get_json_from_file(self, file_name: str) -> dict:
        """Get JSON from file.

        Return dictionary filled with JSONs data.

        Returns:
        --------
            Return dictionary filled with data from file_name

        Raises:
        -------
            FileNotFoundError:
                An error occured when the file is not found
            OSError:
                An error occured during opening the file
            BaseException:
                Base exception if others could not catch the exception
        """
        try:
            with open(file_name, mode='r', encoding="utf-8") as opened_file:
                json_data = json.load(opened_file)

                # In Json there is a property for sorting keys (sort_Keys=True (False by default)),
                # so there is no need in this:
                # return OrderedDict(sorted(json_data.items()))
                return json_data
        except FileNotFoundError:
            print("Could not found the file: %s" % file_name)
        except OSError:
            print("OSError occurred trying open the file: %s" % file_name)
        except BaseException as exception:
            print("BaseException occurred trying open the file: %s" % file_name)
            print(exception)

    def write_json_to_file(self, file_name: str, json_data: dict) -> None:
        """Write JSON to file.

        Write json_data (dictionary) to file_name

        Args:
        -----
            json_data: dict
                Dictionary with JSON-data

        Raises:
        -------
            FileNotFoundError:
                An error occured when the file is not found
            OSError:
                An error occured during opening the file
            BaseException:
                Base exception if others could not the catch exception
        """
        try:
            with open(file_name, mode="w", encoding="utf-8") as opened_file:
                opened_file.write(
                    json.dumps(
                        json_data,
                        indent=2,
                        ensure_ascii=False,
                        sort_keys=True))
        except FileNotFoundError:
            print("Could not found the file: %s" % file_name)
        except OSError:
            print("OSError occurred trying write to the file: %s" % file_name)
        except BaseException as exception:
            print("BaseException occurred trying write to the file: %s" % file_name)
            print(exception)

    @classmethod
    def get_name_from_dict(cls, data: dict) -> str:
        """Gets predefined params from data

        Return string with predefined parameters which was found in data. Predefined
        parameters starts and ends with "__"

        Args:
        -----
            json_data: dict
                Dictionary from JSON

        Returns:
        --------
            Return string with predefined parameters which was found in data.
            Predefied parameters are: "name", "group" and "description".
            If parameters was not found it returns default string
            which is "__Object__"
        """
        if isinstance(data, dict):
            output_string = TRANSLATE_JSONPARSING.gettext("Object")

            ordered_dict = OrderedDict()
            ordered_dict[TRANSLATE_JSONPARSING.gettext("Name")] = data.get(
                'name', None)
            ordered_dict[TRANSLATE_JSONPARSING.gettext("Group")] = data.get(
                'group', None)
            filtered_dict = {key: value for key, value in ordered_dict.items() if value is not None}

            ordered_dict.clear()
            ordered_dict.update(filtered_dict)

            if len(ordered_dict) > 0:
                output_string = ";  ".join(["%s: %s" % (key, value)
                                            for (key, value) in ordered_dict.items()])
            return output_string
        if isinstance(data, list):
            pass
        if isinstance(data, tuple):
            pass

    def translate(self, input_string: str, language: str) -> str:
        """Translates input string to another language.

        Translated from utils.translate.json file

        Args:
        -----
            input_string: str
                Input string to translae
            language: str
                Language to translate

        Raises:
        -------
            KeyError:
                If input_string is not in dictionary

        Returns:
        --------
            Return translated string
        """
        try:
            file_name = os.path.join(
                os.path.split(
                    os.path.abspath(__file__))[0], "locale/translate.json")
            translate_dictionary = self.get_json_from_file(file_name)
            if language == "en":
                return next((key for key, value in translate_dictionary.items()
                             if value == input_string), input_string)
            elif language == "ru":
                return translate_dictionary[input_string]
            else:
                return
        except KeyError:
            return input_string
