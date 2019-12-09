import collections
import enum
import inspect
import typing

INPUT = """
1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1101,0,3,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1102,252,1,1023,1102,36,1,1008,1102,24,1,1017,1101,25,0,1013,1102,479,1,1026,1101,0,259,1022,1102,1,38,1001,1102,1,713,1024,1101,0,708,1025,1102,1,22,1006,1101,0,32,1010,1101,476,0,1027,1102,1,516,1029,1102,1,34,1009,1101,0,23,1016,1102,1,37,1011,1102,525,1,1028,1101,0,35,1004,1102,31,1,1002,1102,39,1,1019,1102,28,1,1015,1102,1,1,1021,1101,0,30,1007,1101,0,27,1014,1101,21,0,1018,1101,0,29,1005,1102,26,1,1000,1102,1,0,1020,1101,0,20,1012,1101,33,0,1003,109,13,21108,40,40,6,1005,1019,199,4,187,1106,0,203,1001,64,1,64,1002,64,2,64,109,15,1205,-7,221,4,209,1001,64,1,64,1105,1,221,1002,64,2,64,109,-25,1208,-3,26,63,1005,63,243,4,227,1001,64,1,64,1106,0,243,1002,64,2,64,109,25,2105,1,-5,1001,64,1,64,1106,0,261,4,249,1002,64,2,64,109,-4,21108,41,42,-8,1005,1016,281,1001,64,1,64,1106,0,283,4,267,1002,64,2,64,109,-6,1206,2,301,4,289,1001,64,1,64,1105,1,301,1002,64,2,64,109,-4,21102,42,1,2,1008,1016,42,63,1005,63,323,4,307,1106,0,327,1001,64,1,64,1002,64,2,64,109,-7,2108,35,1,63,1005,63,343,1105,1,349,4,333,1001,64,1,64,1002,64,2,64,109,-13,1208,7,35,63,1005,63,369,1001,64,1,64,1106,0,371,4,355,1002,64,2,64,109,24,21102,43,1,-1,1008,1017,42,63,1005,63,391,1105,1,397,4,377,1001,64,1,64,1002,64,2,64,109,-13,2101,0,-4,63,1008,63,38,63,1005,63,419,4,403,1105,1,423,1001,64,1,64,1002,64,2,64,109,21,1206,-5,435,1106,0,441,4,429,1001,64,1,64,1002,64,2,64,109,-22,21101,44,0,10,1008,1014,44,63,1005,63,463,4,447,1105,1,467,1001,64,1,64,1002,64,2,64,109,25,2106,0,-2,1106,0,485,4,473,1001,64,1,64,1002,64,2,64,109,-19,2107,37,-2,63,1005,63,501,1106,0,507,4,491,1001,64,1,64,1002,64,2,64,109,8,2106,0,10,4,513,1001,64,1,64,1105,1,525,1002,64,2,64,109,-6,21107,45,46,0,1005,1012,547,4,531,1001,64,1,64,1105,1,547,1002,64,2,64,109,-5,1202,-1,1,63,1008,63,21,63,1005,63,567,1105,1,573,4,553,1001,64,1,64,1002,64,2,64,109,2,1207,-3,21,63,1005,63,589,1105,1,595,4,579,1001,64,1,64,1002,64,2,64,109,1,1201,-8,0,63,1008,63,34,63,1005,63,619,1001,64,1,64,1106,0,621,4,601,1002,64,2,64,109,-6,2102,1,-1,63,1008,63,33,63,1005,63,643,4,627,1105,1,647,1001,64,1,64,1002,64,2,64,109,10,21101,46,0,3,1008,1017,43,63,1005,63,667,1106,0,673,4,653,1001,64,1,64,1002,64,2,64,109,-13,2102,1,8,63,1008,63,35,63,1005,63,697,1001,64,1,64,1106,0,699,4,679,1002,64,2,64,109,23,2105,1,0,4,705,1105,1,717,1001,64,1,64,1002,64,2,64,109,-1,1205,-3,729,1106,0,735,4,723,1001,64,1,64,1002,64,2,64,109,-15,2101,0,0,63,1008,63,38,63,1005,63,755,1106,0,761,4,741,1001,64,1,64,1002,64,2,64,109,-2,2107,28,-1,63,1005,63,779,4,767,1106,0,783,1001,64,1,64,1002,64,2,64,109,-2,2108,35,0,63,1005,63,801,4,789,1105,1,805,1001,64,1,64,1002,64,2,64,109,1,1201,-5,0,63,1008,63,26,63,1005,63,831,4,811,1001,64,1,64,1105,1,831,1002,64,2,64,109,-5,1207,5,30,63,1005,63,849,4,837,1106,0,853,1001,64,1,64,1002,64,2,64,109,2,1202,-2,1,63,1008,63,26,63,1005,63,879,4,859,1001,64,1,64,1105,1,879,1002,64,2,64,109,15,21107,47,46,0,1005,1017,899,1001,64,1,64,1105,1,901,4,885,4,64,99,21102,1,27,1,21101,915,0,0,1106,0,922,21201,1,66416,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21102,942,1,0,1105,1,922,21202,1,1,-1,21201,-2,-3,1,21102,1,957,0,1105,1,922,22201,1,-1,-2,1105,1,968,22102,1,-2,-2,109,-3,2105,1,0
""".strip().split(',')

OPCODE_LENGTH = 2


class HaltException(Exception):
    pass


class WaitForInputException(Exception):
    pass


class Mode(enum.Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class OperationArgument(typing.NamedTuple):
    value: int
    mode: Mode = Mode.POSITION


class IntcodeComputer:
    def __init__(self, memory, inputs=None):
        self.memory = self._initialize_memory(memory)
        self.position = 0
        self.relative_base = 0
        self.inputs = collections.deque(inputs or [])
        self.outputs = collections.deque()

        self.opcodes = {
            1: self.op_add,
            2: self.op_multiply,
            3: self.op_store,
            4: self.op_output,
            5: self.op_jump_if_true,
            6: self.op_jump_if_false,
            7: self.op_less_than,
            8: self.op_equals,
            9: self.op_relative_base_offset,
            99: self.op_halt,
        }

    @classmethod
    def _initialize_memory(cls, memory):
        memory_with_defaults = collections.defaultdict(int)
        for i, val in enumerate(memory):
            memory_with_defaults[i] = val
        return memory_with_defaults


    def compute(self):
        while True:
            op, arguments = self.next_op()

            try:
                advance = op(*arguments)
            except HaltException:
                break

            if advance:
                self.advance(len(arguments) + 1)

    def next_op(self):
        current_val = self.memory[self.position]

        opcode = self.opcode_from_value(current_val)

        try:
            op = self.opcodes[opcode]
        except KeyError:
            raise ValueError(f"Unexpected opcode {opcode} at position {self.position}")

        num_args = self.count_args(op)

        arg_values = [self.memory[i] for i in range(self.position+1, self.position+num_args+1)]
        modes = self.modes_from_value(current_val, fill=num_args)

        return op, [
            OperationArgument(value, mode)
            for value, mode
            in zip(arg_values, modes)
        ]

    def memory_address(self, argument):
        if argument.mode == Mode.POSITION:
            return argument.value
        if argument.mode == Mode.RELATIVE:
            return self.relative_base + argument.value
        raise ValueError("Cannot determine memory address for immediate mode.")

    def value(self, argument):
        if argument.mode in (Mode.POSITION, Mode.RELATIVE):
            return self.memory[self.memory_address(argument)]
        if argument.mode == Mode.IMMEDIATE:
            return argument.value
        raise ValueError(f"Unknown mode {argument.mode}.")

    def advance(self, distance):
        self.position += distance

    @staticmethod
    def count_args(op):
        return len(inspect.signature(op).parameters)

    @staticmethod
    def opcode_from_value(value):
        return int(str(value)[-OPCODE_LENGTH:])

    @staticmethod
    def modes_from_value(value, fill):
        return map(Mode, map(int, reversed(str(value)[:-OPCODE_LENGTH].zfill(fill))))

    # -- Opcode functions below: --

    def op_add(self, param_a, param_b, output):
        self.memory[self.memory_address(output)] = self.value(param_a) + self.value(param_b)
        return True

    def op_multiply(self, param_a, param_b, output):
        self.memory[self.memory_address(output)] = self.value(param_a) * self.value(param_b)
        return True

    def op_store(self, output):
        try:
            self.memory[self.memory_address(output)] = self.inputs.popleft()
        except IndexError:
            raise WaitForInputException
        return True

    def op_output(self, param):
        self.outputs.append(self.value(param))
        return True

    def op_jump_if_true(self, param_a, param_b):
        if self.value(param_a):
            self.position = self.value(param_b)
            return False
        return True

    def op_jump_if_false(self, param_a, param_b):
        if not self.value(param_a):
            self.position = self.value(param_b)
            return False
        return True

    def op_less_than(self, param_a, param_b, output):
        if self.value(param_a) < self.value(param_b):
            self.memory[self.memory_address(output)] = 1
        else:
            self.memory[self.memory_address(output)] = 0
        return True

    def op_equals(self, param_a, param_b, output):
        if self.value(param_a) == self.value(param_b):
            self.memory[self.memory_address(output)] = 1
        else:
            self.memory[self.memory_address(output)] = 0
        return True

    def op_relative_base_offset(self, param):
        self.relative_base += self.value(param)
        return True

    @staticmethod
    def op_halt():
        raise HaltException


def part1():
    instructions = list(map(int, INPUT))

    computer = IntcodeComputer(instructions, inputs=[1])
    computer.compute()

    return computer.outputs.pop()


def part2():
    instructions = list(map(int, INPUT))

    computer = IntcodeComputer(instructions, inputs=[2])
    computer.compute()

    return computer.outputs.pop()


if __name__ == '__main__':
    print(part1())
    print(part2())
