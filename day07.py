import collections
import enum
import inspect
import itertools
import sys
import typing

INPUT = """
3,8,1001,8,10,8,105,1,0,0,21,38,47,64,89,110,191,272,353,434,99999,3,9,101,4,9,9,102,3,9,9,101,5,9,9,4,9,99,3,9,1002,9,5,9,4,9,99,3,9,101,2,9,9,102,5,9,9,1001,9,5,9,4,9,99,3,9,1001,9,5,9,102,4,9,9,1001,9,5,9,1002,9,2,9,1001,9,3,9,4,9,99,3,9,102,2,9,9,101,4,9,9,1002,9,4,9,1001,9,4,9,4,9,99,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,99
""".strip().split(',')

OPCODE_LENGTH = 2


class HaltException(Exception):
    pass


class WaitForInputException(Exception):
    pass


class Mode(enum.Enum):
    POSITION = 0
    IMMEDIATE = 1


class OperationArgument(typing.NamedTuple):
    value: int
    mode: Mode = Mode.POSITION


class IntcodeComputer:
    def __init__(self, memory, inputs=None):
        self.memory = memory
        self.position = 0
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
            99: self.op_halt,
        }

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

        arg_values = self.memory[self.position+1:self.position+num_args+1]
        modes = self.modes_from_value(current_val, fill=num_args)

        return op, [
            OperationArgument(value, mode)
            for value, mode
            in zip(arg_values, modes)
        ]

    def value(self, argument):
        if argument.mode == Mode.POSITION:
            return self.memory[argument.value]
        if argument.mode == Mode.IMMEDIATE:
            return argument.value
        raise ValueError(f"Unknown mode {mode}.")

    def advance(self, distance):
        self.position += distance

    def count_args(cls, op):
        return len(inspect.signature(op).parameters)

    def opcode_from_value(cls, value):
        return int(str(value)[-OPCODE_LENGTH:])

    def modes_from_value(cls, value, fill):
        return map(Mode, map(int, reversed(str(value)[:-OPCODE_LENGTH].zfill(fill))))

    # -- Opcode functions below: --

    def op_add(self, param_a, param_b, output):
        self.memory[output.value] = self.value(param_a) + self.value(param_b)
        return True

    def op_multiply(self, param_a, param_b, output):
        self.memory[output.value] = self.value(param_a) * self.value(param_b)
        return True

    def op_store(self, output):
        try:
            self.memory[output.value] = self.inputs.popleft()
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
            self.memory[output.value] = 1
        else:
            self.memory[output.value] = 0
        return True

    def op_equals(self, param_a, param_b, output):
        if self.value(param_a) == self.value(param_b):
            self.memory[output.value] = 1
        else:
            self.memory[output.value] = 0
        return True

    def op_halt(self):
        raise HaltException


def part1():
    max_output = -sys.maxsize

    for phases in itertools.permutations(range(5)):
        last_output = 0

        for phase in phases:
            instructions = list(map(int, INPUT))

            computer = IntcodeComputer(instructions, inputs=[phase, last_output])
            computer.compute()

            last_output = computer.outputs.pop()

        if last_output > max_output:
            max_output = last_output

    return max_output


def part2():
    max_output = -sys.maxsize

    for phases in itertools.permutations(range(5, 10)):
        last_output = 0
        computers_by_phase = {}

        for phase in itertools.cycle(phases):
            if phase not in computers_by_phase:
                computers_by_phase[phase] = IntcodeComputer(
                    memory=list(map(int, INPUT)),
                    inputs=[phase],
                )

            computer = computers_by_phase[phase]
            computer.inputs.append(last_output)
            try:
                computer.compute()
            except WaitForInputException:
                pass

            try:
                last_output = computer.outputs.pop()
            except IndexError:
                break

        if last_output > max_output:
            max_output = last_output

    return max_output


if __name__ == '__main__':
    print(part1())
    print(part2())
