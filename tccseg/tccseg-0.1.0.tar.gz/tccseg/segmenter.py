import sys

import arguments
from core import Core



class Segmenter(Core):
    def __init__(self, args):
        err_msgs = []
        if args.execute_mode == 'segment':
            if not args.input_data:
                msg = 'Error: the following argument is required for {} mode: {}'.format(args.execute_mode, '--input_data')
                err_msgs.append(msg)

        elif args.execute_mode == 'interactive':
            pass

        else:
            msg = 'Error: invalid execute mode: {}'.format(args.execute_mode)
            err_msgs.append(msg)

        if err_msgs:
            for msg in err_msgs:
                print(msg, file=sys.stderr)
            sys.exit()

        self.args = args
        super().__init__(args.cclib)


    def run_segment_mode(self):
        input_data = self.args.input_data
        res = self.segment(input_data)
        print(res, file=sys.stderr)


    def run_interactive_mode(self):
        print('Please input text or type \'q\' to quit this mode:')
        while True:
            line = sys.stdin.readline().rstrip(' \t\n')
            if len(line) == 0:
                continue
            elif line == 'q':
                break

            res = self.segment(line)
            print(res, file=sys.stderr)



if __name__ == '__main__':
    parser = arguments.ArgumentLoader()
    args = parser.parse_args()

    segmenter = Segmenter(args)
    if args.execute_mode == 'segment':
        segmenter.run_segment_mode()
    elif args.execute_mode == 'interactive':
        segmenter.run_interactive_mode()
