# JSONEditor

## Table of Context

- [About the Project](#about-the-project)
- [Getting Started](#getting-started)
  * [Prerequirements](#prerequirements)
- [Feautures](#feautures)
- [Usage](#usage)
- [Authors](#authors)

## About the Project

Configurations for various projects are stored in JSON files, each of which can be up to a thousand lines in size. Of course, you can edit small JSON documents using ordinary text editors such as Notepad++ or Sublime Text, but if the file reaches thousands of lines or more, it becomes difficult and almost impossible to understand the file structure.
Based on the foregoing, it was decided to develop the JsonToGUI program, which solves the problems posed and allows you to conveniently create new and edit existing JSON files. The JsonToGUI program was developed under Astra Linux OS, but it is expected that the program will work under any OS that has Python3+ version installed.

##  Getting Started

The project was written in `Python 3.5` language using `Qt Creator 3.5.1`. In this regard, for a successful launch, you must use at least these versions. In addition, the following libraries were used in the development process:

### Prerequirements

 - gettext
```
pip install python-gettext
```

## Feautures

- Opening an existing JSON file
- Editing a JSON file: 
  - Adding new elements and their sub-elements (strings, numeric values, booleans, objects and lists); 
  - Deleting items; 
  - Opening the second window of the program if the element name of the first column has the name "file" and the element name of the third column matches the standard JSON file extension (example_name.json)
- Opening a JSON file from under the program
- Saving the changes made in the program to an opened JSON file
- "Save as" file
- "Updating" the file by loading the file again into the program
- Expanding tree elements to several specified levels:
  - Compress tree elements;
  - Expand all items;
  - Expand to 1, 2 or 3 child levels
- Changing the color of root objects, lists and other types to several predefined colors: No color; Yellow; Orange; Red; Green; Blue; Purple; Gray
- Search for specified information in a JSON file with the ability to search in a case-sensitive manner and search in the entire tree or only in the column "Value"
- Support for two languages ​​of the program interface and QTreeVeiw items language:
  - Russian;
  - English
- Support for a standard set of shortcuts

## Usage

`Screenshots example`

## Authors

[Volohov Leonid](https://github.com/LeonidVolohov)
