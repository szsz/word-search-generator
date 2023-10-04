"""
Generates a word search from a list of words.
"""
# Copyright (C) 2020 Tom Saunders

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import time
import string
import random
import argparse
from collections import deque

import numpy

class WordSearch:
   

    def run_generator_from_stdin(self, use_key=False, use_csv=False, folder=None, language=None):
        """Gets data from stdin and then creates a word search"""
        raw_data = _ingest_stdin()
        dimensions = _get_dimensions(raw_data)
        lang = _get_language(raw_data)
        if language:
            lang = language
        words = _get_words(raw_data)

        key, board = generate_word_search(words, lang, dimensions)
        options = {
            "use_key": use_key,
            "output": "file" if folder else "stdout",
            "folder": folder,
            "use_csv": use_csv,
        }
        _export(board, key, dimensions, options)

    @staticmethod
    def _ingest_stdin() -> list:
        """Ingest data from stdin"""
        if sys.stdin.buffer:
            with sys.stdin.buffer as stdin_handler:
                return stdin_handler.read().decode().splitlines()
        else:
            with sys.stdin as stdin_handler:
                return stdin_handler.read().splitlines()

    @staticmethod
    def _get_dimensions(raw_data: list) -> tuple:
        """Get the width and height of the word search"""
        dimension_list = raw_data[0].split(" ")
        if len(dimension_list) != 2:
            raise ValueError(
                "Header containing word search dimensions is invalid. Correct usage - Ex: 2 12"
            )
        try:
            width = int(dimension_list[0])
            height = int(dimension_list[1])
        except ValueError:
            raise ValueError(
                "Width and Height in Header must be integers. Ex: 2 4"
            ) from None
        return (width, height)

    @staticmethod
    def _get_language(raw_data: list) -> str:
        """Get the language of the word search"""
        lang = raw_data[1]
        return lang

    @staticmethod
    def _get_words(raw_data: list) -> list:
        """Gets a list of words"""
        return raw_data[2:]
    
    def __init__(self):
        return
    
    def __init__(self, filename:string):
        
        # opening the file in read mode
        my_file = open(filename, mode="r", encoding="utf-8")
        
        # reading the file
        data = my_file.read()
        
        # replacing end splitting the text 
        # when newline ('\n') is seen.
        raw_data = data.split("\n")
        my_file.close()
        self.dimensions = self._get_dimensions(raw_data)
        self.lang = self._get_language(raw_data)
        self.words = self._get_words(raw_data)



    def generate_word_search(self, trycount: int) -> None:
        """Generate the word search"""
        if not isinstance(self.words, list):
            raise ValueError("words must provide a list of words")
        for word in self.words:
            if not isinstance(word, str):
                raise ValueError("Each word in words must be a string")
        if not isinstance(self.lang, str):
            raise ValueError("lang must provide a valid language string")
        if not isinstance(self.dimensions, (tuple, list)):
            raise ValueError(
                "dimensions must provide a tuple of integers. ex: (width, height)"
            )
        for dimension in self.dimensions:
            if not isinstance(dimension, int):
                raise ValueError("dimension in dimensions must be an integer")
        self._validate_word_length(self.words, self.dimensions)
        self.character_set = self._get_lang_characters(self.lang)
        self.words = self._conform_characters(self.words)
        self.bv = -1
        self.key = None
        self.shortkey = []
        self.board = None
        for g in range(trycount):
            w, sk,k, b, val = self._run_simulation(self.character_set,self.words,self.dimensions)
            if val>self.bv:
                self.bv = val
                self.key = k
                self.shortkey = sk
                self.board = b 
                self.words = w

    def get_res(self) -> tuple:
        b = numpy.copy(self.board)
        b = numpy.insert(b,0,range(1,self.dimensions[0]+1),1)
        b = numpy.insert(b,0,range(0,self.dimensions[1]+1),0)
        return (self.shortkey, self.words,b.tolist(),self.key.tolist())

    @staticmethod
    def _validate_word_length(words: list, dimensions: tuple) -> None:
        """Validate character counts against dimensions"""
        max_characters = dimensions[0] * dimensions[1]
        for word in words:
            if len(word) > dimensions[0] and len(word) > dimensions[1]:
                raise ValueError(
                    "Length of word is greater than the dimensions provided: "
                    + f"{word} - {dimensions}"
                )

    @staticmethod
    def _conform_characters(words: list) -> list:
        """Uppercase all letters"""
        return [word.upper() for word in words]

    @staticmethod
    def _get_lang_characters(lang: str) -> list:
        """Get the language specific character set"""
        if lang == "en":
            return string.ascii_uppercase
        elif lang == "de":
            return string.ascii_uppercase + "ẞÄÖÜ"
        elif lang == "hu":
            return string.ascii_uppercase + "ÁÉÖŐÓÜŰÚÍ"

    @staticmethod
    def _find_pos_for_word(word:str, dimensions:tuple, board:numpy.array) -> tuple:
        """finds a position and directions ((x,y),(dx,dy)) for a new word"""
        options = []
        w = []
        for direction in [(-1,0), (1,0),(-1,1),(-1,-1),(1,1),(1,-1),(0,-1),(0,1)]:
            for x in range(0, dimensions[0]):
                for y in range(0, dimensions[1]):
                    start_point = (x,y)
                    end_point = WordSearch._get_end_point(word, direction, start_point)
                    if WordSearch._detected_edge_collision(dimensions, end_point):
                        continue
                    weight = WordSearch._detected_word_collision(word, direction, board, start_point)
                    if weight > 0:
                        w.append(pow(80,weight))
                        options.append(((x,y),direction))
        if len(options) == 0:
            raise ValueError(
                    "cloud not find solution for word: " + word
                )
        res = random.choices(options,weights=w, k=1)
        return res[0]
        






    @staticmethod
    def _run_simulation(character_set,words,dimensions) -> tuple:
        """Simulate the word search board"""
        board = WordSearch._wipe_board(words, dimensions)
        val = 0
        sk = []
        w = words.copy()
        random.shuffle(w)
        for word in w:        
            (start_point,direction) = WordSearch._find_pos_for_word(word,dimensions,board)
            val = val + WordSearch._save_word(word, direction, start_point, board)
            sk.append("{0} {1} {2} {3} {4}".format(word,start_point[0]+1,start_point[1]+1,direction[0],direction[1]))
        sys.stdout.write(f"\r   \n")
        key = WordSearch._render_whitespace(board.copy())
        board = WordSearch._render_noise(character_set, board, dimensions)
        return w, sk, key, board, val

    @staticmethod
    def _wipe_board(words: list, dimensions: tuple) -> tuple:
        """Get Fresh numpy array and repeat counter"""
        board = WordSearch._get_empty_board(dimensions)
        return board

    @staticmethod
    def _get_empty_board(dimensions: tuple) -> numpy.array:
        """Instantiate the board"""
        width = dimensions[0]
        height = dimensions[1]
        arr = numpy.full(width * height, fill_value=None).reshape(width, height)
        return arr




    @staticmethod
    def _choose_direction() -> tuple:
        """Pick a direction for the word"""
        return random.choice([(-1,0), (1,0),(-1,1),(-1,-1),(1,1),(1,-1),(0,-1),(0,1)])

    @staticmethod
    def _get_end_point(word: str, direction: tuple, start_point: tuple) -> tuple:
        """Get the endpoint for word, direction and start point"""
        x, y = start_point
        length = len(word)
        return x+(length-1)*direction[0],y+(length-1)*direction[1]
    
    @staticmethod
    def _detected_edge_collision(dimensions: tuple, end_point: tuple,) -> bool:
        """Detects if word collides with edge of board"""
        x2, y2 = end_point
        width, height = dimensions
        if x2 <= width - 1 and x2 >= 0 and y2 <= height - 1 and y2 >= 0:
            return False
        return True

    @staticmethod
    def _detected_word_collision(
        word: str, direction: tuple, board: numpy.array, start_point: tuple
    ) -> int:
        """Detects if word collides with another word"""
        x, y = start_point
        weight = 1
        dx, dy = direction
        for increment, character in enumerate(word):
            cell = board[x + increment*dx][y+increment*dy] 
            if not cell:
                continue       
            if cell != character:
                return 0
            else:
                wieght = weight + 1
        return weight

    @staticmethod
    def _save_word(
        word: str, direction: tuple, start_point: tuple, board: numpy.array
    ) -> int:
        val = 0
        dx, dy = direction
        """Saves the word's position"""
        x, y = start_point
        for increment, character in enumerate(word):
            if not board[x + increment*dx][y+increment*dy]:            
                board[x + increment*dx][y+increment*dy] = character
            else:
                val = val+1
        return val

    @staticmethod
    def _render_whitespace(board: numpy.array) -> numpy.array:
        """Substitute None for whitespace"""
        return numpy.where(board == None, " ", board)

    @staticmethod
    def _render_noise(
        character_set: str, board: numpy.array, dimensions: tuple
    ) -> numpy.array:
        """Substitute whitespace for random letters"""
        for row in range(dimensions[0]):
            for column in range(dimensions[1]):
                if not board[row][column]:
                    board[row][column] = random.choice(character_set)
        return board


    def _export(
        board: numpy.array, key: numpy.array, dimensions: tuple, options: dict = {}
    ) -> None:
        """Export the board to a variety of outputs"""
        defaults = {"use_key": False, "output": "stdout", "folder": None, "use_csv": False}
        config = {**defaults, **options}
        if config["output"] == "stdout":
            if config["use_key"]:
                print("Key")
                _send_to_stdout(key, dimensions, config["use_csv"])
                print("")
            print("Board")
            _send_to_stdout(board, dimensions, config["use_csv"])
        elif config["output"] == "file":
            if not os.path.exists(config["folder"]):
                os.makedirs(config["folder"], exist_ok=True)

            extension = "csv" if config["use_csv"] else "txt"
            if config["use_key"]:
                key_filename = os.path.join(
                    config["folder"],
                    f"{os.path.basename(config['folder'])}_key.{extension}",
                )
                _write_to_file(key, dimensions, key_filename, config["use_csv"])
            board_filename = os.path.join(
                config["folder"],
                f"{os.path.basename(config['folder'])}_word_search.{extension}",
            )
            _write_to_file(board, dimensions, board_filename, config["use_csv"])


    def _send_to_stdout(
        board: numpy.array, dimensions: tuple, use_csv: bool = False
    ) -> None:
        """Send board, row by row to stdout"""
        for row in range(dimensions[1]):
            row_string = ""
            for column in range(dimensions[0]):
                row_string += f"{board[row][column]}{',' if use_csv else ' '}"
            print(row_string[:-1])


    def _write_to_file(
        board: numpy.array, dimensions: tuple, filename: str, use_csv: bool = False
    ) -> None:
        """Send board, row by row to stdout"""
        with open(filename, "wb+") as file:
            for row in range(dimensions[1]):
                row_string = ""
                for column in range(dimensions[0]):
                    row_string += f"{board[row][column]}{',' if use_csv else ' '}"
                try:
                    row = f"{row_string}\n".encode()
                    file.write(row)
                except UnicodeEncodeError:
                    print(row_string)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a word search from stdin")
    parser.add_argument(
        "-k", "--key", action="store_true", help="Generate a word search and its key"
    )
    parser.add_argument(
        "--language",
        action="store",
        choices=["en", "de", "hu"],
        help="Choose a language for the word search",
    )
    parser.add_argument(
        "-c",
        "--csv",
        action="store_true",
        help="Return data as csv. Defaults to False. Save to file with -o.",
    )
    parser.add_argument(
        "-o",
        "--output",
        action="store",
        help="Output to file. Specifies the folder name and partial "
        + "filename. Ex: -o ./out -> ./out/out_word_search.csv Defaults to stdout.",
    )
    args = parser.parse_args()
    run_generator_from_stdin(
        use_key=args.key, language=args.language, use_csv=args.csv, folder=args.output
    )
