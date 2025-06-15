import unittest
from tests.test_tool_elderly_wait_time_ccs import TestElderlyWaitTimeCCS

def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestElderlyWaitTimeCCS))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = suite()
    runner.run(test_suite)
