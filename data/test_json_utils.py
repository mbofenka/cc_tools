import test_data
import sys
import json

class Platform:
    def __init__(self, name="Unknown", launch_year=0):
        self.name = name
        self.launch_year = launch_year

class Game:
    def __init__(self, title="Unknown", platform=None, year=0):
        self.title = title
        self.platform = platform
        self.year = year

class GameLibrary:
    def __init__(self):
        self.games = []

    def add_game(self, game):
        self.games.append(game)


def print_game_library(game_library_data):
    print("Analyising game library data:")
    game_count = 0
    for game in game_library_data.games:
        print("  Game "+str(game_count))
        print("    Title = "+game.title)
        print("    Year  = "+str(game.year))
        print("    Platform = ")
        print("       Name = "+game.platform.name)
        print("       Launch Year = "+str(game.platform.launch_year))
        game_count += 1

def make_game_library_from_json(json_data):
    #Initialize a new GameLibrary
    game_library = test_data.GameLibrary()

    #Loop through the json_data
        #Create a new Game object from the json_data by reading
        #  title
        #  year
        #  platform (which requires reading name and launch_year)
        #Add that Game object to the game_library
    #Return the completed game_library

    return game_library

# Handling command line arguments
#  Note: sys.argv is a list of strings that contains each command line argument
#        The first element in the list is always the name of the python file being run
# Command line format: <input json filename>

default_input_json_file = "data/test_data.json"

if len(sys.argv) == 2:
    input_json_file = sys.argv[1]
    print("Using command line args:", input_json_file)
else:
    print("Unknown command line options. Using default values:", default_input_json_file)
    input_json_file = default_input_json_file

#Load the json data from the input file
#Use make_game_library_from_json(json_data) to convert the data to GameLibrary data
#Print out the resulting GameLibrary data using print_game_library(game_library_data) in test_data.py

lib = make_game_library_from_json("test_data.json")
print_game_library(lib)
