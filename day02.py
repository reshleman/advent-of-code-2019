import itertools

INPUT = """
1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,6,19,1,19,6,23,2,23,6,27,2,6,27,31,2,13,31,35,1,9,35,39,2,10,39,43,1,6,43,47,1,13,47,51,2,6,51,55,2,55,6,59,1,59,5,63,2,9,63,67,1,5,67,71,2,10,71,75,1,6,75,79,1,79,5,83,2,83,10,87,1,9,87,91,1,5,91,95,1,95,6,99,2,10,99,103,1,5,103,107,1,107,6,111,1,5,111,115,2,115,6,119,1,119,6,123,1,123,10,127,1,127,13,131,1,131,2,135,1,135,5,0,99,2,14,0,0
""".strip().split(',')


def compute(instructions):
    for i in itertools.count(start=0, step=4):
        opcode = instructions[i]

        if opcode == 1:
            first, second, third = instructions[i+1:i+4]
            instructions[third] = instructions[first] + instructions[second]
        elif opcode == 2:
            first, second, third = instructions[i+1:i+4]
            instructions[third] = instructions[first] * instructions[second]
        elif opcode == 99:
            break
        else:
            raise ValueError(f"Unexpected opcode {opcode} at position {i}")

    return instructions


def part1():
    instructions = list(map(int, INPUT))

    instructions[1] = 12
    instructions[2] = 2

    return compute(instructions)[0]


def part2():
    for noun in range(0, 100):
        for verb in range(0, 100):
            instructions = list(map(int, INPUT))

            instructions[1] = noun
            instructions[2] = verb

            if compute(instructions)[0] == 19690720:
                return noun, verb, 100 * noun + verb


if __name__ == '__main__':
    print(part1())
    print(part2())
