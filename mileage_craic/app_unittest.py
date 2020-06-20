#! /usr/local/bin/python3


import unittest, run


class TestScript(unittest.TestCase):

    def test_password_practice(self):
        self.assertEqual(run.password_practice("testing", "password"), True)
        self.assertEqual(run.password_practice("testing", "testing"), True)
        self.assertEqual(run.password_practice("testing", "free"), False)














"""
now go to terminal and run:
python3 -m unittest app_unittest.py

"""

# to run from directly within editor:
# https://www.youtube.com/watch?v=sugvnHA7ElY

if __name__ == '__main__':
    #this means: if module is run directly (not imported), run code within conditional
    unittest.main()

    #this will run the test