"""
Author: Raymond Xu
Date: January 1, 2025
"""
import unittest
import get

class TestParsePrerequisites(unittest.TestCase):
    def test_one_nonote(self):
        """
        only one course
        """
        text = "MATH 1110 or equivalent."
        self.assertEqual(get.parse_prerequisites(text), [["MATH1110"],False])

    def test_multiple(self):
        """
        multiple courses
        """
        text = (
        "CS 4620 or equivalent; MATH 1120,  MATH 1920, or equivalent; "
        "MATH 2210, MATH 2940, or equivalent; PHYS 1112 or equivalent."
        )
        expected = [['MATH2210', 'MATH2940'], ['MATH1120', 'MATH1920'],
        ['CS4620'], ['PHYS1112'],False]
        self.assertCountEqual(get.parse_prerequisites(text), expected)

    def test_parentheses(self):
        """
        with parentheses
        """
        text = (
        "probability theory (e.g. BTRY 3080, CS 2800, ECON 3130, "
        "ENGRD 2700, MATH 4710) and linear algebra (e.g. MATH 2210, "
        "MATH 2310, MATH 2940), single-variable calculus (e.g. MATH 1110, "
        "MATH 1920) and programming proficiency (e.g. CS 2110)."
        )

        expected = [['BTRY3080', 'CS2800', 'ECON3130', 'ENGRD2700', 'MATH4710'],
        ['MATH2210', 'MATH2230', 'MATH2310', 'MATH2940'], ['MATH1910',
        'MATH1120'], ['CS2110', 'CS2112'],True]
        self.assertCountEqual(get.parse_prerequisites(text), expected)

    def test_for(self):
        """
        with for...majors...
        """
        text = ("Elementary Python (ex. CS 1133), LING 1101 or CS 2800 or "
        "PHIL 2310; for CS majors: Elementary Python and CS 2800.")
        expected = [['CS1110', 'CS1112', 'CS1133'],
        ['LING1101', 'CS2800', 'PHIL2310'],True]
        self.assertCountEqual(get.parse_prerequisites(text), expected)

    def test_or(self):
        """
        with A, B, C, or D
        """
        text = ("MATH 2210, MATH 2230, MATH 2310, MATH 2940, or equivalent.")
        expected = [['MATH2210', 'MATH2230', 'MATH2310', 'MATH2940'],False]
        self.assertCountEqual(get.parse_prerequisites(text), expected)

    def test_note(self):
        """
        with "Note:" and "1)..."
        """
        text = ("1) linear algebra: strong performance in MATH 2940 or "
        "equivalent; 2) discrete math: strong performance in CS 2800 or "
        "equivalent. Note: the linear algebra and discrete math requirements "
        "can also be fulfilled with a strong performance in INFO 2950; and "
        "3) programming proficiency: CS 2110 or equivalent with strong "
        "Python skills and familiarity with IPython Notebooks, or "
        "permission of instructor.")

        expected = [['MATH2210', 'MATH2230', 'MATH2310', 'MATH2940'],
        ['CS2800'], ['CS2110', 'CS2112'],True]
        self.assertCountEqual(get.parse_prerequisites(text), expected)

    def test_middle(self):
        """
        with "-"
        """
        text = ("MATH 1110-MATH 1120 with high performance, equivalent AP "
        "credit, or permission of department.")
        expected = [['MATH1120'],True]
        self.assertCountEqual(get.parse_prerequisites(text), expected)

    def test_instructor(self):
        """
        remove ", or permission of the instructor."
        """
        text = ("MATH 2210 or MATH 2940 or equivalent, knowledge of "
        "programming, CS 3220 or CS 4210/MATH 4250, or permission of "
        "the instructor. ")
        expected = [['CS1110', 'CS1112', 'CS1132', 'CS1133'],
        ['MATH2210', 'MATH2940'], ['CS3220', 'CS4210', 'MATH4250'],True]
        self.assertCountEqual(get.parse_prerequisites(text), expected)

    def test_dash(self):
        """
        text with "--"
        """
        text =  ("a good level of programming experience--specifically, the "
        "ability to deal with challenging programming tasks--familiarity with "
        "common algorithms and data structures, and an understanding of basic "
        "concepts in discrete mathematics.")
        expected = [['CS2110','CS2112'],['CS2800'],True]
        self.assertCountEqual(get.parse_prerequisites(text), expected)

    def test_repeat(self):
        """
        cases with repeat courses (CS 2800)
        """
        text = ("CS 2800, probability theory (e.g. BTRY 3010, ECON 3130, "
        "MATH 4710, ENGRD 2700), linear algebra (e.g. MATH 2940), calculus "
        "(e.g. MATH 1920), programming proficiency (e.g. CS 2110), and CS 3780 "
        "or equivalent or permission of instructor.")
        expected = [['CS2800'], ['CS3780'], ['MATH2210', 'MATH2230', 'MATH2310',
         'MATH2940'], ['MATH1920', 'MATH2220', 'MATH2240'],
         ['CS2110', 'CS2112'], ['BTRY3080', 'ECON3130',
         'ENGRD2700', 'MATH4710'],True]
        self.assertCountEqual(get.parse_prerequisites(text), expected)

    def test_replace_programming(self):
        """
        need `programming course` replacement
        """
        text = "one programming course or equivalent programming experience."
        expected = [['CS1110', 'CS1112', 'CS1132', 'CS1133'],True]
        self.assertCountEqual(get.parse_prerequisites(text), expected)


if __name__ == "__main__":
    unittest.main()
