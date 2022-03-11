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


if __name__ == '__main__':
    unittest.main()
