import unittest
from unittest.mock import patch
from linker import linker

class TestLinker(unittest.TestCase):

    @patch('linker.music.music')
    def test_music_keywords(self, mock_music):
        for keyword in ['play', 'pause', 'stop', 'next', 'previous']:
            category = linker(f"Please {keyword} the song")
            self.assertEqual(category, 'music player')
            mock_music.assert_called_once()
            mock_music.reset_mock()

    @patch('linker.timer.timer')
    def test_timer_keywords(self, mock_timer):
        # Test all timer keywords
        for keyword in ['set timer', 'start timer', 'stop timer', 'set a timer', 'start a timer', 'stop the timer']:
            category = linker(f"Could you {keyword} for 5 minutes?")
            self.assertEqual(category, 'timer')
            mock_timer.assert_called_once()
            mock_timer.reset_mock()

    @patch('linker.search.search')
    def test_search_keywords(self, mock_search):
        # Test all search keywords
        for keyword in ['search', 'find', 'lookup']:
            category = linker(f"Can you {keyword} this?")
            self.assertEqual(category, 'search')
            mock_search.assert_called_once()
            mock_search.reset_mock()

if __name__ == '__main__':
    unittest.main()
