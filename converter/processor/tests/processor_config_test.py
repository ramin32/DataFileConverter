import unittest
import StringIO

from converter.processor import processor
from converter.processor import processor_config

class TestProcessorConfig(unittest.TestCase):

    def setUp(self):
        yaml_file = StringIO.StringIO('''
        csv:
            mapping:
                classroom id: classroom_id
                student_grade: grade_id

            shareable_siblings: teacher parent 

        hierachy: 
            grade:
                classroom:
                    teacher:
                    student: ''')
        self.config = processor_config.ProcessorConfig(yaml_file)
        
        blank_yaml_file = StringIO.StringIO('')
        self.blank_config = processor_config.ProcessorConfig(blank_yaml_file)


    def test_map_field(self):
        output = self.config.map_field(processor.CsvProcessor, 'classroom id')
        field = 'classroom_id'
        self.assertEqual(field, output)

        output = self.config.map_field(processor.CsvProcessor, 'asdf')
        field = 'asdf'
        self.assertEqual(field, output)


    def test_hierachy(self):
        hierachy = {'grade': {'classroom': {'teacher': None, 'student': None}}}
        output = self.config.hierachy()
        self.assertEqual(hierachy, output)

        with self.assertRaises(processor_config.ConfigError):
            self.blank_config.hierachy()

    def test_shareable_siblings(self):
        siblings = ['teacher', 'parent']
        output =  self.config.shareable_siblings(processor.CsvProcessor)
        self.assertEqual(siblings, output)

        with self.assertRaises(processor_config.ConfigError):
            self.blank_config.shareable_siblings(processor.CsvProcessor)

if __name__ == '__main__':
    unittest.main()

