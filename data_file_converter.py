#!/usr/bin/python2.7

import argparse
from converter import converter

def parse_args():
    parser = argparse.ArgumentParser(description='Convert files of different formats.')

    for a in ['--in-file','--out-file', '--in-format-file', '--out-format-file', 
            '--in-format-type','--out-format-type', '--config-file']:
        parser.add_argument(a, required=True)

    return parser.parse_args()


def main():
    args = parse_args() 

    with open(args.in_format_file, 'rb') as in_format_file, \
         open(args.out_format_file, 'rb') as out_format_file, \
         open(args.config_file, 'rb') as config_file, \
         open(args.in_file, 'rb') as in_file, \
         open(args.out_file, 'wb') as out_file:

        c = converter.Converter(in_format_file, 
                                args.in_format_type, 
                                out_format_file, 
                                args.out_format_type, 
                                config_file) 
        c.convert(in_file, out_file)

if __name__ == "__main__":
    main()

