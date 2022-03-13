import sys
from chunk import Chunk
from enum import Enum
from math import ceil
from operator import mul
from typing import List, Any


# https://docs.python.org/3/library/enum.html
class LineStatus(Enum):
    ParsedSuccessfully = 1
    Corrupted = 2
    Incomplete = 3


class ProcessLineResult:
    def __init__(self, line_status: LineStatus, failure_index: int = None, unclosed_tags: List[int] = None):
        self._line_status = line_status
        self._failure_index = failure_index
        self._unclosed_tags = unclosed_tags

    def line_status(self):
        return self._line_status

    def failure_index(self):
        return self._failure_index

    def unclosed_tags(self):
        return self._unclosed_tags

    @staticmethod
    def success_result():
        return ProcessLineResult(LineStatus.ParsedSuccessfully)

    @staticmethod
    def corrupted_result(failure_index: int):
        return ProcessLineResult(LineStatus.Corrupted, failure_index=failure_index)

    @staticmethod
    def incomplete_result(unclosed_tags: List[int]):
        return ProcessLineResult(LineStatus.Incomplete, unclosed_tags=unclosed_tags)


# https://docs.python.org/3/tutorial/classes.html
class Chunk:
    def __init__(self, start_character: str, start_index: int, parent: Chunk = None):
        self._start_character = start_character
        self._start_index = start_index
        self._end_character = None
        self._end_index = None
        self._parent = parent

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

    def try_end_chunk(self, end_character: str, end_index: int):
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


def get_error_score(line: str, character_index: int) -> int:
    error_character = line[character_index]

    match error_character:
        case ')':
            return 3
        case ']':
            return 57
        case '}':
            return 1197
        case '>':
            return 25137


def get_completion_string(line: str, uncompleted_indexes: List[int]) -> str:
    # In C# I might consider using a StringBuilder or a string join here
    completion_string = ""

    for uncompleted_index in reversed(uncompleted_indexes):
        start_character = line[uncompleted_index]

        match start_character:
            case '<':
                completion_string += '>'
            case '(':
                completion_string += ')'
            case '{':
                completion_string += '}'
            case '[':
                completion_string += ']'

    return completion_string


def get_completion_string_score(completion_string: str) -> int:
    score = 0

    for character in completion_string:
        score = mul(score, 5)

        match character:
            case ')':
                score += 1
            case ']':
                score += 2
            case '}':
                score += 3
            case '>':
                score += 4

    return score


def get_exercise_lines() -> List[str]:
    # https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
    with open("exercise_part_one_input.txt", 'r') as f:
        read_data = f.read()

    file_lines = read_data.split("\n")

    return file_lines


def get_middle_list_item(items_list: List[Any]) -> Any:
    middle_item_index = ceil(len(items_list) / 2) - 1  # Compensate for the fact lists are zero indexed

    return items_list[middle_item_index]


def process_line(line: str) -> ProcessLineResult:
    current_chunk: Chunk = None

    parsed_chunks: List[Chunk] = []

    for line_index in range(len(line)):
        match line[line_index]:
            case '<' | '{' | '(' | '[':
                if current_chunk is None:
                    current_chunk = Chunk(line[line_index], line_index)

                    parsed_chunks.append(current_chunk)

                    continue

                child_chunk = Chunk(line[line_index], line_index, current_chunk)

                parsed_chunks.append(child_chunk)

                current_chunk = child_chunk

                continue

            case '>' | '}' | ')' | ']':

                if current_chunk is not None and current_chunk.try_end_chunk(line[line_index], line_index):
                    current_chunk = current_chunk.parent()

                    continue

                return ProcessLineResult.corrupted_result(line_index)

        break

    # If we get to this point then we haven't found any rogue end tags, do we have any unclosed chunks

    unclosed_chunk_indexes = []

    for parsed_chunk in parsed_chunks:
        if isinstance(parsed_chunk, Chunk) and parsed_chunk.end_index() is None:
            unclosed_chunk_indexes.append(parsed_chunk.start_index())

    if any(unclosed_chunk_indexes):
        return ProcessLineResult.incomplete_result(unclosed_chunk_indexes)

    return ProcessLineResult.success_result()  # If we reach here then all pairs were successfully matched


if __name__ == '__main__':
    syntax_score = 0

    completion_string_scores = []

    exercise_lines = get_exercise_lines()

    for exercise_line in exercise_lines:
        result = process_line(exercise_line)

        if result.line_status() == LineStatus.Corrupted:
            syntax_score += get_error_score(exercise_line, result.failure_index())

        elif result.line_status() == LineStatus.Incomplete:
            line_completion_string = get_completion_string(exercise_line, result.unclosed_tags())

            line_completion_string_score = get_completion_string_score(line_completion_string)

            completion_string_scores.append(line_completion_string_score)

    even_count_completion_scores = divmod(len(completion_string_scores), 2) == 0

    if even_count_completion_scores:  # Panic, chaos, something has gone wrong
        # https://docs.python.org/3/library/sys.html#sys.exit
        sys.exit(1)

    sorted_completion_scores = sorted(completion_string_scores)

    middle_completion_string_score = get_middle_list_item(sorted_completion_scores)

    print(f"Syntax error score {syntax_score}")

    print(f"Middle completion error score {middle_completion_string_score}")