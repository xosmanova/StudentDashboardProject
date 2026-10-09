"""
test_services.py
Unit tests for business logic functions: calculate_grade and calculate_statistics.
Ensures 100% correctness of grading boundaries and KPI calculations.
"""

import unittest
from services import calculate_grade, calculate_statistics, validate_student_input


class TestBusinessLogic(unittest.TestCase):

    def test_calculate_grade_exact_assignment_examples(self):
        """Tests exact score examples specified in project prompt."""
        self.assertEqual(calculate_grade(91.0), "A")
        self.assertEqual(calculate_grade(85.0), "B")
        self.assertEqual(calculate_grade(72.0), "C")
        self.assertEqual(calculate_grade(63.0), "D")
        self.assertEqual(calculate_grade(48.0), "F")

    def test_calculate_grade_boundary_values(self):
        """Tests threshold boundaries for all letter grades."""
        self.assertEqual(calculate_grade(100.0), "A")
        self.assertEqual(calculate_grade(90.0), "A")
        self.assertEqual(calculate_grade(89.9), "B")
        self.assertEqual(calculate_grade(80.0), "B")
        self.assertEqual(calculate_grade(79.9), "C")
        self.assertEqual(calculate_grade(70.0), "C")
        self.assertEqual(calculate_grade(69.9), "D")
        self.assertEqual(calculate_grade(60.0), "D")
        self.assertEqual(calculate_grade(59.9), "F")
        self.assertEqual(calculate_grade(0.0), "F")

    def test_calculate_grade_invalid_ranges(self):
        """Ensures ValueError is raised when score is out of 0-100 range."""
        with self.assertRaises(ValueError):
            calculate_grade(-1.0)

        with self.assertRaises(ValueError):
            calculate_grade(101.0)

    def test_calculate_statistics_assignment_dataset(self):
        """Tests statistics on sample dataset from assignment prompt."""
        students = [
            {"Name": "Ali", "Score": 85.0},
            {"Name": "Leyla", "Score": 72.0},
            {"Name": "Murad", "Score": 48.0},
            {"Name": "Aysel", "Score": 91.0},
            {"Name": "Kamran", "Score": 63.0},
        ]
        stats = calculate_statistics(students)

        self.assertEqual(stats["total_students"], 5)
        self.assertAlmostEqual(stats["average_score"], 71.8, places=1)
        self.assertEqual(stats["highest_score"], 91.0)
        self.assertEqual(stats["lowest_score"], 48.0)

    def test_calculate_statistics_empty_dataset(self):
        """Tests safe defaults on empty list."""
        stats = calculate_statistics([])
        self.assertEqual(stats["total_students"], 0)
        self.assertEqual(stats["average_score"], 0.0)
        self.assertEqual(stats["highest_score"], 0.0)
        self.assertEqual(stats["lowest_score"], 0.0)

    def test_validate_student_input(self):
        """Tests input validation rules."""
        is_valid, _ = validate_student_input("Ali", 85.0)
        self.assertTrue(is_valid)

        is_valid, msg = validate_student_input("", 85.0)
        self.assertFalse(is_valid)
        self.assertIn("empty", msg)

        is_valid, msg = validate_student_input("A", 85.0)
        self.assertFalse(is_valid)
        self.assertIn("at least 2 characters", msg)

        is_valid, msg = validate_student_input("Valid Name", 150.0)
        self.assertFalse(is_valid)


if __name__ == "__main__":
    unittest.main()
