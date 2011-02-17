import csv
from lxml import etree
import re

import processor_util

class IProcessor(object):
    '''Processor interface for parsing and writing a format.
       etree.Element objects are used for data encapsulation.'''

    ID = None

    def __init__(self, format_file, config=None):
        pass
    def parseFromFile(self, input_file):
        pass
    def writeToFile(self, data, output_file):
        pass

class CsvProcessor(IProcessor):
    ID = 'csv'

    def __init__(self, format_file, config):
        header = csv.reader(format_file).next()
        self.field_names = [config.map_field(self, name.strip()) for name in header]
        self.config = config

    def parseFromFile(self, input_file):
        data_dict_list = [d for d in csv.DictReader(input_file, self.field_names)]
        elements = processor_util.dict_list_to_elements(data_dict_list, 
                                                        self.field_names, 
                                                        self.config.hierachy(),
                                                        self.config.shareable_siblings(self))

        if len(elements) == 1:
            return elements[0]
        raise etree.XMLSyntaxError('Csv creates multiple roots!')

    def writeToFile(self, root_element, output_file):
        data_dict_list = processor_util.element_to_dict_list(root_element, self.config.shareable_siblings(self))

        writer = csv.DictWriter(output_file, self.field_names, extrasaction='ignore')
        writer.writerows(data_dict_list)

class XmlProcessor(IProcessor):
    ID = 'xml'

    def __init__(self, format_file, config=None):
        schema_root = etree.parse(format_file)
        self.xml_schema = etree.XMLSchema(schema_root)
        try:
            self.namespace = schema_root.getroot().attrib['targetNamespace']
        except KeyError:
            raise etree.XMLSchemaError("No target namespace in xml schema!")

    def parseFromFile(self, input_file):
        root_element = etree.parse(input_file).getroot()
        if not self.xml_schema.validate(root_element):
            raise etree.XMLSchemaValidateError("Couldn't validate input xml!")
        return root_element

    def writeToFile(self, root_element, output_file):
        root_element.attrib['xmlns'] = self.namespace #set root namespace to the one found in the schema

        # TODO figure out a way to create valid xmls from incompatible formats
        # if not self.xml_schema.validate(root_element):
        #    raise etree.XMLSchemaValidateError("Cannon write invalid xml!")

        tree = etree.ElementTree(root_element)
        tree.write(output_file, pretty_print=True, encoding='iso-8859-1')



