import argparse
import sys



class ArgumentLoader(object):
    def __init__(self):
        # self.parser = argparse.ArgumentParser()
        pass


    def parse_args(self):
        all_args = self.get_full_parser().parse_args()
        min_args = self.get_minimum_parser(all_args).parse_args()
        return min_args


    def get_full_parser(self):
        parser = argparse.ArgumentParser()

        ### mode options
        parser.add_argument('--execute_mode', '-x', choices=['segment', 'interactive'], help='Choose a mode from among \'segment\' and \'interactive\'')

        ### data paths and related options
        parser.add_argument('--input_data', '-i', help='Input data (text)')
        parser.add_argument('--cclib', choices=['original', 'cfcc'], default='original', help='Specify Character Cluster library from among \'original\' and \'cfcc\' (Default: original)')

        return parser


    def get_minimum_parser(self, args):
        parser = argparse.ArgumentParser()

        # basic options
        self.add_basic_options(parser, args)

        # dependent options
        if args.execute_mode == 'segment':
            self.add_segment_mode_options(parser, args)
        elif args.execute_mode == 'interactive':
            self.add_interactive_mode_options(parser, args)
        else:
            print('Error: invalid execute mode: {}'.format(args.execute_mode), file=sys.stderr)
            sys.exit()

        return parser


    def add_basic_options(self, parser, args):
        # mode options
        parser.add_argument('--execute_mode', '-x', required=True, default=args.execute_mode)


    def add_segment_mode_options(self, parser, args):
        # data paths and related options
        parser.add_argument('--input_data', '-i', required=True, default=args.input_data)
        parser.add_argument('--cclib', default=args.cclib)


    def add_interactive_mode_options(self, parser, args):
        # data paths and related options
        parser.add_argument('--cclib', default=args.cclib)
