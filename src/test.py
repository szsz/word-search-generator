# Import the code to be tested
import unittest   # The test framework
import sys
import wordSearchGenerator

class Test_TestIncrementDecrement(unittest.TestCase):
   

    def test_en(self):        
        sys.stdin = open("./tests/sample_data_english.txt", "r")
        wordSearchGenerator.run_generator_from_stdin(False, False, None, language="en")

    def test_en(self):        
        sys.stdin = open("./tests/sample_data_hun.txt", "r")
        wordSearchGenerator.run_generator_from_stdin(True, False, None, language="hu")

if __name__ == '__main__':
    unittest.main()