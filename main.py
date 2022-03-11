from enum import Enum

corruptedLines = [
    "{([(<{}[<>[]}>{[]{[(<()>",
    "[[<[([]))<([[{}[[()]]]",
    "[{[{({}]{}}([{[{{{}}([]",
    "[<(<(<(<{}))><([]([]()",
    "<{([([[(<>()){}]>(<<{{"
]

allLines = [
    "[({(<(())[]>[[{[]{<()<>>",
    "[(()[<>])]({[<{<<[]>>(",
    "{([(<{}[<>[]}>{[]{[(<()>",
    "(((({<>}<{<{<>}{[]{[]{}",
    "[[<[([]))<([[{}[[()]]]",
    "[{[{({}]{}}([{[{{{}}([]",
    "{<[[]]>}<{[{[{[]{()[[[]",
    "[<(<(<(<{}))><([]([]()",
    "<{([([[(<>()){}]>(<<{{",
    "<{([{{}}[<[[[<>{}]]]>[]]",
    "([{<({<[{<([])>}]>})>}])"
    # Added a valid line just to make sure that this works - will be covered in Unit Tests in the full solution
]


# https://docs.python.org/3/library/enum.html
class LineStatus(Enum):
    ParsedSuccessfully = 1
    Corrupted = 2
    Incomplete = 3


# https://docs.python.org/3/tutorial/classes.html
class Chunk:
    def __init__(self, start_character, start_index):
        self._start_character = start_character
        self._start_index = start_index
        self._end_character = None
        self._end_index = None

    def __init__(self, start_character, start_index, parent):
        self._parent = parent
        self.__init__(start_character, start_index)

    def start_character(self):
        return self._start_character

    def start_index(self):
        return self._start_index

    def end_character(self):
        return self._end_character

    def end_index(self):
        return self._end_index

    def parent(self):
        return self._parent

    def try_end_chunk(self, end_character, end_index):
        # https://docs.python.org/3/tutorial/controlflow.html
        # Python match does not fall through cases and you don't seem to be able to use
        # alternation with a guard clause - refactor to if
        if ((end_character == '>' and self._start_character == '<')
                or (end_character == '}' and self._start_character == '{')
                or (end_character == ')' and self._start_character == '(')
                or (end_character == ']' and self._start_character == '[')):
            self._end_character = end_character
            self._end_index = end_index
            return True

        return False
