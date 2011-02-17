#!/usr/bin/python2.7
import unittest

from converter.processor.tests import processor_util_test
from converter.processor.tests import processor_config_test



suite = unittest.TestSuite()

for test in [processor_util_test, processor_config_test]:
    suite.addTests(unittest.TestLoader().loadTestsFromModule(test))

unittest.TextTestRunner(verbosity=2).run(suite)


