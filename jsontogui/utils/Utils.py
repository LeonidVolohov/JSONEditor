"""This module does basic operations to prepare or check data for further analysis.

    Typical usage example:
    ----------------------

    utils = Utils()
    utils.get_abs_file_path("test.json")
    utils.file_name_match("test.json")
    utils.string_to_boolean("True.json")

    print(Utils().get_abs_file_path("test.json"))
"""
import os
import re

from utils.translate import translate_dictionary


class Utils():
    """Class for for the necessary functions needed during process of preparing data for the GUI.

    Attributes:
    -----------
    None

    Methods:
    --------
    get_abs_file_path(file_name: str) -> str:
        Return absolute path for given file_name with project path where it started from

    file_name_match(file_name: str) -> bool:
        Return True if given file_name match .json file extension

    string_to_boolean(input_string: str) -> bool
        Return True if input_string is "True" False if "False"
    translate(input_string: str, language: str) -> str:
        Return translated input_string from translate.py dictionary
    """

    def __init__(self) -> None:
        """Constructs all the necessary attributes for the Utils object.

        Args:
        -----
            None
        """
        pass

    @classmethod
    def get_abs_file_path(cls, file_name: str) -> str:
        """Return abs path for given file_name.

        Return absolute path for give input file_name. Joins project path with given file_name.

        Args:
        -----
            file_name: str
                Input file_name of file or file_name with its file_path

        Returns:
        --------
            Join given input file name or file path + file name and path of project
            from where the project was started. For example: file_name is "example.json"
            and file was started from "/home/user/project/utils/" it would return
            "/home/user/project/example.json". Or if file_name was "someFolder/example.json"
            it would retrun "/home/user/project/someFolder/example".

        Raises:
        -------
            OSError:
                An error occured during os execution.
        """
        try:
            script_path = os.path.abspath(__file__)             # ../JsonToGUI/utils/JsonParsing.py
            script_dir = os.path.split(script_path)[0]          # ../JsonToGUI/utils/
            script_dir = os.path.dirname(script_dir)            # ../JsonToGUI/
            abs_file_path = os.path.join(script_dir, file_name)

            return abs_file_path
        except OSError as exception:
            print("OSError occurred: %s" % exception)
        except BaseException as exception:
            print("Unexpected exception: %s" % exception)

    @classmethod
    def file_name_match(cls, file_name: str) -> bool:
        """Check if given file_name match for .jsons file extension.

        Function check if given file_name matches for the standard .json extension.
        File could not be ".json" (with an empty name, where there is only file extension).

        Args:
        -----
            file_name: str
                Input json file_name

        Returns:
        --------
            Return True if file_name match, False if not

        Raises:
        -------
            re.error:
                Exception raised when a string passed to one of the functions
                here is not a valid regular expression or when some other error
                occurs during compilation or matching.

        """
        try:
            return True if re.search(r"\w\.json$", file_name) else False
        except re.error:
            return False

    @classmethod
    def string_to_boolean(cls, input_string: str) -> bool:
        """Convert input string to boolean

        Can`t use eval() due to user can load anything and eval still return False.

        Args:
        -----
            input_string: str
                Input string with "True" or "False" value

        Returns:
        --------
            Return True if input_string is "True" False if "False".
        """
        if input_string == "True":
            return True
        elif input_string == "False":
            return False
        else:
            return

    @classmethod
    def translate(cls, input_string: str, language: str) -> str:
        """Translates input string to another language

        Translated from translate.translate_dictionary dictionary from utils/translate file

        Args:
        -----
            input_string: str
                Input string to translae
            language:
                Language to translate

        Raises:
        -------
            KeyError:
                If input_string is not in dictionary


        Returns:
        --------
            Return True if input_string is "True" False if "False".
        """
        try:
            if language == "en":
                return next((key for key, value in translate_dictionary.items()
                    if value == input_string), input_string)
            elif language == "ru":
                return translate_dictionary[input_string]
            else:
                return
        except KeyError as exception:
            return input_string
