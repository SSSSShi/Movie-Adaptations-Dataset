import sys
import os
import unittest
from unittest.mock import patch, MagicMock

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.goodreads import clean_number, clean_name, extract_float_safely, get_page_url

class TestGoodreadsScraper(unittest.TestCase):
    def test_clean_number(self):
        """Test the clean_number function with various inputs"""
        self.assertEqual(clean_number("1,234,567"), 1234567)
        self.assertEqual(clean_number("1234"), 1234)
        self.assertEqual(clean_number("invalid"), 0)
        self.assertEqual(clean_number(""), 0)

    def test_clean_name(self):
        """Test the clean_name function with various inputs"""
        self.assertEqual(clean_name('"Test Book"'), "Test Book")
        self.assertEqual(clean_name('Normal Book'), 'Normal Book')
        self.assertEqual(clean_name(''), '')

    def test_extract_float_safely(self):
        """Test the extract_float_safely function"""
        mock_match = MagicMock()
        mock_match.group.return_value = "4.5"
        self.assertEqual(extract_float_safely(mock_match), 4.5)
        self.assertEqual(extract_float_safely(None), 0.0)

    @patch('requests.get')
    def test_url_formation(self, mock_get):
        """Test URL formation for different pages"""
        from src.goodreads import get_page_url
        base_url = "https://www.goodreads.com/list/show/17956.Best_Movie_Adaptations"
        self.assertEqual(get_page_url(base_url, 1), base_url)
        self.assertEqual(get_page_url(base_url, 2), f"{base_url}?page=2")

if __name__ == '__main__':
    unittest.main()
