import enum
import inspect
import typing

INPUT = """
3,225,1,225,6,6,1100,1,238,225,104,0,1101,37,61,225,101,34,121,224,1001,224,-49,224,4,224,102,8,223,223,1001,224,6,224,1,224,223,223,1101,67,29,225,1,14,65,224,101,-124,224,224,4,224,1002,223,8,223,101,5,224,224,1,224,223,223,1102,63,20,225,1102,27,15,225,1102,18,79,224,101,-1422,224,224,4,224,102,8,223,223,1001,224,1,224,1,223,224,223,1102,20,44,225,1001,69,5,224,101,-32,224,224,4,224,1002,223,8,223,101,1,224,224,1,223,224,223,1102,15,10,225,1101,6,70,225,102,86,40,224,101,-2494,224,224,4,224,1002,223,8,223,101,6,224,224,1,223,224,223,1102,25,15,225,1101,40,67,224,1001,224,-107,224,4,224,102,8,223,223,101,1,224,224,1,223,224,223,2,126,95,224,101,-1400,224,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,1002,151,84,224,101,-2100,224,224,4,224,102,8,223,223,101,6,224,224,1,224,223,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,108,677,677,224,1002,223,2,223,1006,224,329,101,1,223,223,1107,677,226,224,102,2,223,223,1006,224,344,101,1,223,223,8,677,677,224,1002,223,2,223,1006,224,359,101,1,223,223,1008,677,677,224,1002,223,2,223,1006,224,374,101,1,223,223,7,226,677,224,1002,223,2,223,1006,224,389,1001,223,1,223,1007,677,677,224,1002,223,2,223,1006,224,404,1001,223,1,223,7,677,677,224,1002,223,2,223,1006,224,419,1001,223,1,223,1008,677,226,224,1002,223,2,223,1005,224,434,1001,223,1,223,1107,226,677,224,102,2,223,223,1005,224,449,1001,223,1,223,1008,226,226,224,1002,223,2,223,1006,224,464,1001,223,1,223,1108,677,677,224,102,2,223,223,1006,224,479,101,1,223,223,1108,226,677,224,1002,223,2,223,1006,224,494,1001,223,1,223,107,226,226,224,1002,223,2,223,1006,224,509,1001,223,1,223,8,226,677,224,102,2,223,223,1006,224,524,1001,223,1,223,1007,226,226,224,1002,223,2,223,1006,224,539,1001,223,1,223,107,677,677,224,1002,223,2,223,1006,224,554,1001,223,1,223,1107,226,226,224,102,2,223,223,1005,224,569,101,1,223,223,1108,677,226,224,1002,223,2,223,1006,224,584,1001,223,1,223,1007,677,226,224,1002,223,2,223,1005,224,599,101,1,223,223,107,226,677,224,102,2,223,223,1005,224,614,1001,223,1,223,108,226,226,224,1002,223,2,223,1005,224,629,101,1,223,223,7,677,226,224,102,2,223,223,1005,224,644,101,1,223,223,8,677,226,224,102,2,223,223,1006,224,659,1001,223,1,223,108,677,226,224,102,2,223,223,1005,224,674,1001,223,1,223,4,223,99,226
""".strip().split(',')

OPCODE_LENGTH = 2


class HaltException(Exception):
    pass


class Mode(enum.Enum):
    POSITION = 0
    IMMEDIATE = 1


class OperationArgument(typing.NamedTuple):
    value: int
    mode: Mode = Mode.POSITION


class IntcodeComputer:
    def __init__(self, memory):
        self.memory = memory
        self.position = 0

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
        self.memory[output.value] = int(input("Input: "))
        return True

    def op_output(self, param):
        print(self.value(param))
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


if __name__ == '__main__':
    instructions = list(map(int, INPUT))

    computer = IntcodeComputer(instructions)
    computer.compute()
