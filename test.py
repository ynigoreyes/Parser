import unittest
from Scanner import Scanner
from Parser import Parser
from InvalidTokenExpection import InvalidTokenExpection
from BadTokenExpection import BadTokenExpection

class TestScannerFunctionality(unittest.TestCase):
    def setUp(self):
        print('\n\n\n')

    def test_for_error_on_bad_assignment(self):
        """
        y = 7
        """
        with self.assertRaises(BadTokenExpection):
            parser = Parser('y = 7')
            parser.parse()

    def test_for_print_on_good_assignment(self):
        """
        x := 7
        """
        parser = Parser('x := 7')
        parser.parse()

    def test_for_print_on_read(self):
        """
        read A
        """
        parser = Parser('read A')
        parser.parse()

    def test_for_print_on_write(self):
        """
        write 10 + 12
        """
        parser = Parser('write 10 + 12')
        parser.parse()

    def test_for_print_on_comments(self):
        """
        /**
          * With some kind of comment
          */
        write 0 + 0
        """
        parser = Parser("""
        /**
          * With some kind of comment
          */
        write 0 + 0
        """)
        parser.parse()
            
if __name__ == '__main__':
    unittest.main()