from configparser import ConfigParser

configObject = ConfigParser()

configObject["QTreeView"] = {
	"setAlternatingRowColors": "False",
	"setAnimated": "False",
	
	"expandAll": "False",
	"expandToDepth": "-2", # -2: Dont Expand, -1: ExpandAll, 0: Zero level, ...
}

configObject["Other"] = {
	"defaultJsonFileName": "config_apak.json"
}

configObject["Language"] = {
	"defaultLanguage": "en",		# Language for GUI
	"writeToJsonLanguage": "en" 	# Language for writing back to JSON-file
}

configObject["MainWindow"] = {
	"showMaximized": "False"
}

# configObject[""] = {
# 	"": "",
# 	"": ""	
# }

with open('config.ini', 'w') as config:
	configObject.write(config)
