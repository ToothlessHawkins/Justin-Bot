from io import StringIO
from pprint import pprint
import unittest
import inspect

import testBot


def run_tests():
    test_cases = []
    for name, obj in inspect.getmembers(testBot):
        if inspect.isclass(obj):
            test_cases.append([name, obj])

    stream = StringIO()
    runner = unittest.TextTestRunner(stream=stream)
    output = []
    for pair in test_cases:
        result = runner.run(unittest.makeSuite(pair[1]))
        output.append('Test Suite: {}'.format(pair[0]))
        output.append('Tests run : {}'.format(result.testsRun))
        output.append('Errors {}'.format(result.errors))
        output.append('Failures: {}'.format(result.failures))
        output.append('Test output\n{}'.format(stream.read()))
    return output


def silent_tests():
    test_cases = []
    for name, obj in inspect.getmembers(testBot):
        if inspect.isclass(obj):
            test_cases.append([name, obj])

    stream = StringIO()
    runner = unittest.TextTestRunner(stream=stream)
    output = []
    for pair in test_cases:
        result = runner.run(unittest.makeSuite(pair[1]))
        # same as above but only print if there are failures or errors
        if result.errors or result.failures:
            output.append('Test Suite: {}'.format(pair[0]))
            output.append('Tests run : {}'.format(result.testsRun))
            output.append('Errors {}'.format(result.errors))
            output.append('Failures: {}'.format(result.failures))
            output.append('Test output\n{}'.format(stream.read()))
    return output
