import unittest
from lxml import etree
import os

from converter.processor import processor_util

class TestProcessorConfig(unittest.TestCase):

    def setUp(self):
        pass

    def test_clean_namespace(self):
        string = "{some weird namespace}foobar"
        clean_string = "foobar"
        output = processor_util.clean_namespace(string)

        self.assertEqual(clean_string, output)

    def test_prefix_dictionary_keys(self):
        d = {'a': 1, 'b': 2}
        prefixed_d = {'p_a': 1, 'p_b': 2}

        output = processor_util.prefix_dictionary_keys(d, 'p')
        self.assertEqual(prefixed_d, output)

        prefixed_d = {'p_1_a': 1, 'p_1_b': 2}

        output = processor_util.prefix_dictionary_keys(d, 'p', separator='_1_')
        self.assertEqual(prefixed_d, output)

    def test_remove_prefix(self):
        string = 'foo_bar'
        output = processor_util.remove_prefix(string)
        self.assertEqual(output, 'bar')


if __name__ == '__main__':
    unittest.main()
