# Please do not re-distribute - Henry Xi

import unittest
from StringIO import StringIO
import sys
import os.path
import a1ece650

HighlightBegin = '\x1b[6;30;42m'
HighlightEnd = '\x1b[0m'


def stub_stdin(testcase_inst, inputs):
    stdin = sys.stdin

    def cleanup():
        sys.stdin = stdin

    testcase_inst.addCleanup(cleanup)
    sys.stdin = StringIO(inputs)


def stub_stdouts(testcase_inst):
    stderr = sys.stderr
    stdout = sys.stdout

    def cleanup():
        sys.stderr = stderr
        sys.stdout = stdout

    testcase_inst.addCleanup(cleanup)
    sys.stderr = StringIO()
    sys.stdout = StringIO()


class TestA1(unittest.TestCase):
    def setUp(self):
        self.stdout_array = []
        self.script_output_array = []
        self.script_line_array = []
        self.result_array = []
        self.line_index = 0
        while True:
            self.user_input = raw_input('Enter script filename: ')
            self.user_input = self.user_input.split("--")
            self.file_name = self.user_input[0].replace(' ', '')
            if not os.path.isfile(self.file_name):
                print(HighlightBegin + "Test Error: Cannot Find File in Directory" + HighlightEnd)
            else:
                break

    def tearDown(self):
        sys.stdout.flush()

    def test_runScript(self):
        with open(self.file_name, 'r') as file:
            for line in file:
                self.line_index += 1
                if line[0] == '#' or line[0] == '' or line[0] == '\n':
                    continue
                line_array = line.split(' :: ')
                if len(line_array) != 2:
                    print("Script Error: Unrecognized line " + str(self.line_index))
                    return
                line_array[0] = line_array[0].replace(' ', '')
                line_array[1] = line_array[1].replace('\n', '')
                if line_array[0][:len('LOG')].lower() == str('LOG').lower():
                    self.result_array.append(line_array[1])
                elif line_array[0][:len('INPUT')].lower() == str('INPUT').lower():
                    if line_array[1][0:5].lower() == str('BEGIN').lower():
                        self.stdout_array = []
                    elif line_array[1][:len('END')].lower() == str('END').lower():
                        pass
                    else:
                        stub_stdin(self, line_array[1])
                        stub_stdouts(self)
                        a1ece650.main()
                        std_return = str(sys.stdout.getvalue())
                        self.doCleanups()
                        if std_return != '':
                            std_return = std_return.split('\n')
                            for index in range(len(std_return)):
                                if std_return[index] != '':
                                    self.stdout_array.append(std_return[index])
                elif line_array[0][:len('OUTPUT')].lower() == str('OUTPUT').lower():
                    if line_array[1][0:5].lower() == str('BEGIN').lower():
                        pass
                    elif line_array[1][:len('END')].lower() == str('END').lower():
                        for output in range(len(self.script_output_array)):
                            if self.script_output_array[output] == '' and len(self.stdout_array) == 0:
                                self.result_array.append('LINE: ' + str(self.script_line_array[output]) + ': PASS')
                            elif self.script_output_array[output] in self.stdout_array:
                                self.result_array.append('LINE: ' + str(self.script_line_array[output]) + ': PASS')
                            else:
                                self.result_array.append('LINE: ' + str(self.script_line_array[output]) + ': FAILED')
                        if len(self.script_output_array) == len(self.stdout_array):
                            self.result_array.append(
                                'EXPECTED OUTPUT: ' + str(len(self.script_output_array)) + ' LINES. ' + 'ACTUAL '
                                                                                                        'OUTPUT: ' +
                                str(len(self.stdout_array)) + ' LINES. : PASS')
                        else:
                            self.result_array.append(
                                'EXPECTED OUTPUT: ' + str(len(self.script_output_array)) + ' LINES. ' + 'ACTUAL '
                                                                                                        'OUTPUT: ' +
                                str(len(self.stdout_array)) + ' LINES. : FAILED')
                        for result in range(len(self.result_array)):
                            print(self.result_array[result])

                        for parameter in range(1, len(self.user_input)):
                            if self.user_input[parameter] == 'r':
                                print("Program Response: ")
                                for response in range(len(self.stdout_array)):
                                    print(str(self.stdout_array[response]))
                        self.result_array = []
                        self.script_output_array = []
                        self.script_line_array = []
                    else:
                        self.script_output_array.append(line_array[1])
                        self.script_line_array.append(self.line_index)


if __name__ == '__main__':
    unittest.main()
