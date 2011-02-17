from processor import processor_util
from processor import processor_config


class Converter(object):
    def __init__(self, in_format_file, in_format_type, out_format_file, out_format_type, config_file):
        config = processor_config.ProcessorConfig(config_file)

        self.from_processor = processor_util.create_processor(in_format_type, in_format_file, config)
        self.to_processor = processor_util.create_processor(out_format_type, out_format_file, config)
        self.out_format_type = out_format_type

    def convert(self, in_file, out_file):
        data = self.from_processor.parseFromFile(in_file)
        self.to_processor.writeToFile(data, out_file)
        
