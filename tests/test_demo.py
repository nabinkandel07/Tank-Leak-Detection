import unittest

from src.run_demo import evaluate, simulate


class LeakDetectorTests(unittest.TestCase):
    def test_simulation_length_and_alarm(self):
        rows, predictions = simulate()
        self.assertEqual(len(rows), 240)
        precision, recall, first_detection = evaluate(predictions)
        self.assertEqual(precision, 1.0)
        self.assertGreater(recall, 0.95)
        self.assertEqual(first_detection, 122)


if __name__ == "__main__":
    unittest.main()
