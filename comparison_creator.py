from copy import deepcopy
import re

def nand(a, b):
    return not (a and b)

def mux(a, b, sel):
    if sel == 0:
        return a
    return b

def xor(a, b):
    if a | b and not (a and b):
        return 1
    return 0

def get_nodes():
    inputs = []
    outputs = []
    i = 0
    while True:
        temp = input(f"Input {i+1}: ")
        if temp == 'end':
            break
        inputs.append(temp)
        i += 1
    
    i = 0
    while True:
        temp = input(f"Output {i+1}: ")
        if temp == 'end':
            break
        outputs.append(temp)
        i += 1
    return inputs, outputs

def create_grid(nodes):
    total_grid = []
    inner_grid = []

    for i in range(1, len(nodes) + 1):
        for _ in range(1, 2**len(nodes) + 1, 2**(i-1)*2):
            for _ in range(2**(i-1)):
                inner_grid.append(0)

            for _ in range(2**(i-1)):
                inner_grid.append(1)

        total_grid.append(deepcopy(inner_grid))
        inner_grid.clear()
    return total_grid


def expression_evaluation(grid, inputs, outputs):
    evaluations = []

    for i in range(len(outputs)):
        ogExpression = input(f"What is boolean expression #{i + 1}? ")

        temp = []
        for j in range(len(grid)):
            boolean_expression = deepcopy(ogExpression)
            for count, l in enumerate(inputs):
                pattern = r'\b(?<!\w)' + re.escape(l) + r'(?!\w)\b'
                boolean_expression = re.sub(pattern, str(grid[j][count]), boolean_expression)
            temp.append(int(eval(boolean_expression)))
        evaluations.append(temp)

    return evaluations


def format_grid(grid, inputs, outputs):
    headerGrid = []
    totalSpaces = 7

    for i in grid:
        i.insert(0, '|   ')
        for j in range(2, len(i)*2 - 2, 2):
            i.insert(j, '   |   ')
        i.append('   |')

    headerGrid.append('|')
    for i in range(len(inputs)):
        headerGrid.append(' ' * ((totalSpaces - len(inputs[i])) // 2))
        headerGrid.append(inputs[i])
        headerGrid.append(' ' * ((totalSpaces - len(inputs[i])) // 2) + '|')
    
    for i in range(len(outputs)):
        headerGrid.append(' ' * ((totalSpaces - len(outputs[i])) // 2))
        headerGrid.append(outputs[i])
        headerGrid.append(' ' * ((totalSpaces - len(outputs[i])) // 2) + '|')

    grid.insert(0, headerGrid)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j] = str(grid[i][j])

    return grid

def write_cmp(fileName, grid):
    with open(fileName + '.cmp', 'w') as f:
        for i in grid:
            f.write(i)
            f.write('\n')
    f.close()

# https://stackoverflow.com/questions/8421337/rotating-a-two-dimensional-array-in-python
def rotated(grid):
    list_of_tuples = zip(*grid[::-1])
    return [list(elem) for elem in list_of_tuples]


def write_tst(fileName, inputs, outputs):
    full_out = []

    output_list = '%B3.1.3 '.join(inputs) + '%B3.1.3 ' + '%B3.1.3'.join(outputs) + '%B3.1.3'
    header = f'load {fileName}.hdl,\n' + f'output-file {fileName}.out,\n' + f'compare-to {fileName}.cmp,\n' + f'output-list {output_list};\n\n'

    full_out.append(header)
    temp = ''
    bit_num = format(0, f'0{len(inputs)}b')

    for i in range(2**len(inputs)):
        for j in range(len(inputs)):
            temp += f'set {inputs[j]} {bit_num[j]},\n'
        temp += 'eval,\n'
        temp += 'output;\n\n'
        full_out.append(temp)
        temp = ''
        bit_num = bin_add(bit_num, inputs)
    
    with open(fileName + '.tst', 'w') as f:
        for i in full_out:
            f.write(i)

def bin_add(num, inputs):
    if type(num) == str:
        bit_num = int(num, 2)
    bit_num += 1
    bit_num = format(bit_num, f'0{len(inputs)}b')
    return bit_num


def main():
    inputs, outputs = get_nodes()
    grid = create_grid(inputs)
    grid = rotated(grid)

    evaluations = expression_evaluation(grid, inputs, outputs)
    for i in range(len(outputs)):
        for count, j in enumerate(grid): 
            j.append(evaluations[i][count])

    grid = format_grid(grid, inputs, outputs)

    for i in range(len(grid)):
        grid[i] = ''.join(grid[i])

    fileName = input("What is your .hdl file called? ")    
    write_cmp(fileName, grid)
    write_tst(fileName, inputs, outputs)

if __name__ == '__main__':
    main()