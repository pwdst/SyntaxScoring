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
            with self.subTest(i=i):
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
            with self.subTest(i=i):
                start_tag = start_tags[i]

                end_tag = end_tags[i]

                chunk = main.Chunk(start_tag, 4)

                result = chunk.try_end_chunk(end_tag, 5)

                self.assertFalse(result)

                self.assertIsNone(chunk.end_character())

                self.assertIsNone(chunk.end_index())

if __name__ == '__main__':
    unittest.main()
