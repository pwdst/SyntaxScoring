import unittest
import main


class ChunkTestCase(unittest.TestCase):
    def test_init_with_parent_sets_expected(self):
        parent = main.Chunk('[', 5)

        chunk = main.Chunk('<', 8, parent)

        self.assertEqual('<', chunk.start_character())

        self.assertEqual(8, chunk.start_index())

        self.assertEqual(parent, chunk.parent())

        self.assertIsNone(chunk.end_character())

        self.assertIsNone(chunk.end_index())

    def test_init_without_parent_sets_expected(self):
        chunk = main.Chunk('<', 8)

        self.assertEqual('<', chunk.start_character())

        self.assertEqual(8, chunk.start_index())

        self.assertIsNone(chunk.end_character())

        self.assertIsNone(chunk.end_index())

        self.assertIsNone(chunk.parent())

    def test_try_end_chunk_returns_true_if_matching_tag(self):
        start_tags = ['<', '[', '{', '(']

        end_tags = ['>', ']', '}', ')']

        self.assertEqual(len(start_tags), len(end_tags))

        # todo Is there a better way to do this?
        for i in range(len(start_tags)):
            with self.subTest(i):
                start_tag = start_tags[i]

                end_tag = end_tags[i]

                chunk = main.Chunk(start_tag, 4)

                result = chunk.try_end_chunk(end_tag, 5)

                self.assertTrue(result)

                self.assertEqual(end_tag, chunk.end_character())

                self.assertEqual(5, chunk.end_index())

    def test_try_end_chunk_returns_true_if_different_tag(self):
        start_tags = ['<', '[', '{', '(']

        end_tags = [']', '>', ')', '}']

        self.assertEqual(len(start_tags), len(end_tags))

        # todo Is there a better way to do this?
        for i in range(len(start_tags)):
            with self.subTest(i):
                start_tag = start_tags[i]

                end_tag = end_tags[i]

                chunk = main.Chunk(start_tag, 4)

                result = chunk.try_end_chunk(end_tag, 5)

                self.assertFalse(result)

                self.assertIsNone(chunk.end_character())

                self.assertIsNone(chunk.end_index())


class GetCompletionStringTestCase(unittest.TestCase):
    def test_get_completion_string_returns_expected(self):
        cases = [
            ("[({(<(())[]>[[{[]{<()<>>", [0, 1, 2, 3, 12, 13, 14, 17], "}}]])})]"),
            ("[(()[<>])]({[<{<<[]>>(", [10, 11, 12, 13, 14, 21], ")}>]})"),
            ("(((({<>}<{<{<>}{[]{[]{}", [0, 1, 2, 3, 8, 9, 10, 15, 18], "}}>}>))))"),
            ("{<[[]]>}<{[{[{[]{()[[[]", [8, 9, 10, 11, 12, 13, 16, 19, 20], "]]}}]}]}>"),
            ("<{([{{}}[<[[[<>{}]]]>[]]", [0, 1, 2, 3], "])}>")
        ]

        for case in cases:
            line = case[0]

            with self.subTest(line):
                uncompleted_indexes = case[1]

                expected = case[2]

                result = main.get_completion_string(line, uncompleted_indexes)

                self.assertEqual(expected, result)


class GetCompletionStringScoreTestCase(unittest.TestCase):
    def test_get_completion_string_score_returns_expected(self):
        completion_string_scores = {
            "}}]])})]": 288957,
            ")}>]})": 5566,
            "}}>}>))))": 1480781,
            "]]}}]}]}>": 995444,
            "])}>": 294
        }

        for completion_string in completion_string_scores:
            with self.subTest(completion_string):
                expected_score = completion_string_scores[completion_string]

                result = main.get_completion_string_score(completion_string)

                self.assertEqual(expected_score, result)


class GetErrorScoreTestCase(unittest.TestCase):
    def test_get_error_score_returns_expected(self):
        line = "([{<({<[{<([])>}]>})>}])"

        index_score_dictionary = {
            13: 3,  # )
            14: 25137,  # >
            15: 1197,  # }
            16: 57  # ]
        }

        # todo Is there a better way to do this?
        for index in index_score_dictionary:
            with self.subTest(index):
                expected_score = index_score_dictionary[index]

                result = main.get_error_score(line, index)

                self.assertEqual(expected_score, result)


class ProcessLineTestCase(unittest.TestCase):
    def test_process_line_valid_chunks_successful(self):
        valid_lines = ["([{<({<[{<([])>}]>})>}])"];

        for valid_line in valid_lines:
            result = main.process_line(valid_line)

            self.assertEqual(main.LineStatus.ParsedSuccessfully, result.line_status())

            self.assertIsNone(result.failure_index())

            self.assertIsNone(result.unclosed_tags())

    def test_process_corrupt_line_returns_expected(self):
        corrupt_lines = {"{([(<{}[<>[]}>{[]{[(<()>": 12,
                         "[[<[([]))<([[{}[[()]]]": 8,
                         "[{[{({}]{}}([{[{{{}}([]": 7,
                         "[<(<(<(<{}))><([]([]()": 10,
                         "<{([([[(<>()){}]>(<<{{": 16}

        for corrupt_line in corrupt_lines:
            character_index = corrupt_lines.get(corrupt_line)

            result = main.process_line(corrupt_line)

            self.assertEqual(main.LineStatus.Corrupted, result.line_status())

            self.assertEqual(character_index, result.failure_index())

            self.assertIsNone(result.unclosed_tags())

    def test_process_incomplete_line_returns_expected(self):
        incomplete_lines = {"[({(<(())[]>[[{[]{<()<>>": [0, 1, 2, 3, 12, 13, 14, 17],
                            "[(()[<>])]({[<{<<[]>>(": [10, 11, 12, 13, 14, 21],
                            "(((({<>}<{<{<>}{[]{[]{}": [0, 1, 2, 3, 8, 9, 10, 15, 18],
                            "{<[[]]>}<{[{[{[]{()[[[]": [8, 9, 10, 11, 12, 13, 16, 19, 20],
                            "<{([{{}}[<[[[<>{}]]]>[]]": [0, 1, 2, 3]}

        for incomplete_line in incomplete_lines:
            unclosed_tag_indexes = incomplete_lines[incomplete_line]

            result = main.process_line(incomplete_line)

            self.assertEqual(main.LineStatus.Incomplete, result.line_status())

            self.assertEqual(unclosed_tag_indexes, result.unclosed_tags())

            self.assertIsNone(result.failure_index())


class ProcessLineResultTestCase(unittest.TestCase):
    def test_process_line_success_result(self):
        result = main.ProcessLineResult.success_result()

        self.assertEqual(main.LineStatus.ParsedSuccessfully, result.line_status())

        self.assertIsNone(result.failure_index())

    def test_process_line_success_result(self):
        result = main.ProcessLineResult.corrupted_result(8)

        self.assertEqual(main.LineStatus.Corrupted, result.line_status())

        self.assertEqual(8, result.failure_index())

    def test_process_line_success_result(self):
        result = main.ProcessLineResult.incomplete_result([8, 11, 12])

        self.assertEqual(main.LineStatus.Incomplete, result.line_status())

        self.assertEqual([8, 11, 12], result.unclosed_tags())

        self.assertIsNone(result.failure_index())


if __name__ == '__main__':
    unittest.main()
