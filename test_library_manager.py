import unittest
from library_manager_gui import LibraryManager
from datetime import datetime, timedelta
import os
import json

class TestLibraryManager(unittest.TestCase):

    def setUp(self):
        # Setup a temporary database file
        self.library = LibraryManager('test_library_database.json')
        self.library.books = {}
        self.library.save_data()

    def tearDown(self):
        # Remove the temporary database file after tests
        os.remove('test_library_database.json')

    def test_add_book(self):
        self.library.add_book("Test Book", "Test Author", 2)
        self.assertEqual(len(self.library.books), 1)
        self.assertIn(1, self.library.books)  # Check if book_id 1 is in books

    def test_get_book_info(self):
        self.library.add_book("Test Book", "Test Author", 2)
        book_info = self.library.get_book_info(1)
        self.assertIsNotNone(book_info)
        self.assertEqual(book_info['title'], "Test Book")

    def test_check_out_book(self):
        self.library.add_book("Test Book", "Test Author", 2)
        result = self.library.check_out_book(1)
        self.assertTrue(result)
        self.assertEqual(self.library.books[1]['copies_available'], 1)

    # More test cases for other methods...

if __name__ == '__main__':
    unittest.main()
