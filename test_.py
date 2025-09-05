import unittest
from unittest.mock import patch
from linker import linker
import queue
import threading
import linker


class TestCategoryDetection(unittest.TestCase):
    def test_valid_category(self):
        # Music should map to 'music'
        result = linker.detect_category("play music")
        self.assertEqual(result, "music")

    def test_unknown_category(self):
        # Force an embedding below threshold by patching model
        with patch.object(linker, "model") as mock_model:
            mock_model.encode.return_value = [0.0, 0.0]
            with patch("linker.util.cos_sim", return_value=[[0.0]]):
                result = linker.detect_category("random nonsense")
        self.assertEqual(result, linker.KEYWORD_UNK)


class TestBroadcaster(unittest.TestCase):
    def test_broadcaster_sends_message(self):
        linker_queue = queue.Queue()
        broadcast_qs = {"music": queue.Queue(), "end": queue.Queue()}

        # Patch category_thread_map to avoid KeyError
        linker.category_thread_map = {"music": threading.Thread(target=lambda: None)}

        # Send a fake message
        linker_queue.put({"category": "music", "text": "play song"})

        # Run one iteration of broadcaster
        def run_once():
            msg = linker_queue.get()
            broadcast_qs[msg["category"]].put(msg["text"])

        run_once()

        self.assertEqual(broadcast_qs["music"].get(), "play song")


class TestModuleThreads(unittest.TestCase):
    def test_start_module_threads_creates_threads(self):
        # Fake program functions
        def dummy_program(q):
            while True:
                msg = q.get()
                if msg == "TERMINATE":
                    break

        q1, q2 = queue.Queue(), queue.Queue()
        program_queue_map = {q1: dummy_program, q2: dummy_program}

        threads = linker.start_module_threads(program_queue_map)
        self.assertIsInstance(threads, dict)
        self.assertTrue(all(isinstance(t, threading.Thread) for t in threads.values()))


class TestTermination(unittest.TestCase):
    def test_terminate_message(self):
        broadcast_qs = {"music": queue.Queue(), "timer": queue.Queue()}

        # Put TERMINATE in queues
        for q in broadcast_qs.values():
            q.put("TERMINATE")

        # Simulate a module reading TERMINATE
        def dummy_program(q):
            msg = q.get()
            self.assertEqual(msg, "TERMINATE")

        # Run in threads
        threads = {}
        for name, q in broadcast_qs.items():
            t = threading.Thread(target=dummy_program, args=(q,))
            t.start()
            threads[name] = t

        for t in threads.values():
            t.join(timeout=1)

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

if __name__ == '__linker__':
    unittest.linker()
