#!/usr/bin/env python
#
# Template for MIPS assembler.py
#
# Usage:
#    python assembler.py [asm file]

import sys, re


def bin_to_hex(x):
    y = hex(int(x, 2))[2:]
    if len(y) < 8:
        y = (8 - len(y)) * "0" + y
    return y


def dec_to_bin(value, nbits):
    value = int(value)
    fill = "0"
    if value < 0:
        value = (abs(value) ^ 0xffffffff) + 1
        fill = "1"

    value = bin(value)[2:]
    if len(value) < nbits:
        value = (nbits - len(value)) * fill + value
    if len(value) > nbits:
        value = value[-nbits:]
    return value


rtypes = ['sll',
          'srl',
          'sra',
          'sllv',
          'srlv',
          'srav',
          'jr',
          'jalr',
          'syscall',
          'break',
          'mfhi',
          'mthi',
          'mflo',
          'mtlo',
          'mult',
          'multu',
          'div',
          'divu',
          'add',
          'addu',
          'sub',
          'subu',
          'and',
          'or',
          'xor',
          'nor',
          'slt',
          'sltu']  # List of all R-type instructions.
r_shift = ['sll',
           'srl',
           'sra',
           'sllv',
           'srlv',
           'srav']  # List of all R-type Shift Instructions

op_codes = {'bltz': dec_to_bin(1, 6),
            'j': dec_to_bin(2, 6),
            'jal': dec_to_bin(3, 6),
            'beq': dec_to_bin(4, 6),
            'bne': dec_to_bin(5, 6),
            'blez': dec_to_bin(6, 6),
            'bgtz': dec_to_bin(7, 6),
            'addi': dec_to_bin(8, 6),
            'addiu': dec_to_bin(9, 6),
            'slti': dec_to_bin(10, 6),
            'sltiu': dec_to_bin(11, 6),
            'andi': dec_to_bin(12, 6),
            'ori': dec_to_bin(13, 6),
            'xori': dec_to_bin(14, 6),
            'lui': dec_to_bin(15, 6),
            'mfc0': dec_to_bin(16, 6),
            'bclf': dec_to_bin(17, 6),
            'lb': dec_to_bin(32, 6),
            'lh': dec_to_bin(33, 6),
            'lw': dec_to_bin(35, 6),
            'lbu': dec_to_bin(36, 6),
            'lhu': dec_to_bin(37, 6),
            'sb': dec_to_bin(40, 6),
            'sh': dec_to_bin(41, 6),
            'sw': dec_to_bin(43, 6),
            'lwc1': dec_to_bin(49, 6),
            'swc1': dec_to_bin(56, 6)
            # Fill in mapping from instruction to its opcode.
            }  # List of all Opcodes belonging to a non R-type format

function_codes = {'sll': dec_to_bin(0, 6),
                  'srl': dec_to_bin(2, 6),
                  'sra': dec_to_bin(3, 6),
                  'sllv': dec_to_bin(4, 6),
                  'srlv': dec_to_bin(6, 6),
                  'srav': dec_to_bin(7, 6),
                  'jr': dec_to_bin(8, 6),
                  'jalr': dec_to_bin(9, 6),
                  'syscall': dec_to_bin(12, 6),
                  'break': dec_to_bin(13, 6),
                  'mfhi': dec_to_bin(16, 6),
                  'mthi': dec_to_bin(17, 6),
                  'mflo': dec_to_bin(18, 6),
                  'mtlo': dec_to_bin(19, 6),
                  'mult': dec_to_bin(24, 6),
                  'multu': dec_to_bin(25, 6),
                  'div': dec_to_bin(26, 6),
                  'divu': dec_to_bin(27, 6),
                  'add': dec_to_bin(32, 6),
                  'addu': dec_to_bin(33, 6),
                  'sub': dec_to_bin(34, 6),
                  'subu': dec_to_bin(35, 6),
                  'and': dec_to_bin(36, 6),
                  'or': dec_to_bin(37, 6),
                  'xor': dec_to_bin(38, 6),
                  'nor': dec_to_bin(39, 6),
                  'slt': dec_to_bin(42, 6),
                  'sltu': dec_to_bin(43, 6)
                  # Fill in function codes.
                  }  # List of all function codes of R-Type Instructions

registers = {
    '$zero': dec_to_bin(0, 5),
    '$at': dec_to_bin(1, 5),
    '$v0': dec_to_bin(2, 5),
    '$v1': dec_to_bin(3, 5),
    '$a0': dec_to_bin(4, 5),
    '$a1': dec_to_bin(5, 5),
    '$a2': dec_to_bin(6, 5),
    '$a3': dec_to_bin(7, 5),
    '$t0': dec_to_bin(8, 5),
    '$t1': dec_to_bin(9, 5),
    '$t2': dec_to_bin(10, 5),
    '$t3': dec_to_bin(11, 5),
    '$t4': dec_to_bin(12, 5),
    '$t5': dec_to_bin(13, 5),
    '$t6': dec_to_bin(14, 5),
    '$t7': dec_to_bin(15, 5),
    '$s0': dec_to_bin(16, 5),
    '$s1': dec_to_bin(17, 5),
    '$s2': dec_to_bin(18, 5),
    '$s3': dec_to_bin(19, 5),
    '$s4': dec_to_bin(20, 5),
    '$s5': dec_to_bin(21, 5),
    '$s6': dec_to_bin(22, 5),
    '$s7': dec_to_bin(23, 5),
    '$t8': dec_to_bin(24, 5),
    '$t9': dec_to_bin(25, 5),
    '$k0': dec_to_bin(26, 5),
    '$k1': dec_to_bin(27, 5),
    '$gp': dec_to_bin(28, 5),
    '$sp': dec_to_bin(29, 5),
    '$fp': dec_to_bin(30, 5),
    '$ra': dec_to_bin(31, 5)
    # Fill out the rest of the registers.
}  # List of all registers


def pluck_comment(comment_symbol, line_list):
    if comment_symbol in line_list:
        index1 = line_list.index('#')
        comment = line_list[index1:]
        line_list = line_list[:index1]
        comment = ' '.join(comment)
    else:
        comment = 'No Comments'
    return comment


def seperate_line_components(label_symbol, line_count, line_list, line_attr):
    length = len(line_list)
    line_count = line_count + 1
    # print(our_line_list)
    if label_symbol in line_list[0]:
        line_attr['label'] = line_list[0]
        line_attr['instruction'] = line_list[1]
        # line_attr['arg0']=our_line_list[2]
        if length > 2:
            for i in range(2, length):
                line_list[i] = line_list[i].replace(',', "")
                line_attr[('arg' + str(i - 2))] = line_list[i]

    else:
        line_attr['instruction'] = line_list[0]
        if len(line_list) > 1:
            for i in range(1, length):
                line_list[i] = line_list[i].replace(',', "")
                line_attr[('arg' + str(i - 1))] = line_list[i]
    line_attr['line_number'] = line_count
    return line_attr, line_count


def r_instructions_components(line_attr, line):
    funct = function_codes[(line['instruction'])]
    rd = line['arg0']
    rd = registers[rd]
    op = dec_to_bin(0, 6)
    shamt2 = dec_to_bin(0, 5)
    if line['instruction'] in r_shift:
        rs = dec_to_bin(0, 5)
        rt = line['arg1']
        if rt in registers.keys():
            rt = registers[rt]
        shamt2 = line['arg2']
        shamt2 = dec_to_bin(shamt2, 5)
        # else:
        # print(2)
    elif line['instruction'] == 'jr':
        rs = line['arg0']
        rs = registers[rs]
        rt = dec_to_bin(0, 5)
        rd = dec_to_bin(0, 5)

    else:
        shamt2 = dec_to_bin(0, 5)
        if 'arg1' in line:
            rs = line['arg1']
            rs = registers[rs]
        else:
            rs = dec_to_bin(0, 5)
        if 'arg2' in line:
            rt = line['arg2']
            if rt in registers.keys():
                rt = registers[rt]
            else:
                rt = dec_to_bin(rt, 5)
        else:
            rt = dec_to_bin(0, 5)

    return op, rs, rt, rd, shamt2, funct


def to_stdout(file,machinecode):
    temp = sys.stdout  # store original stdout object for later
    sys.stdout = open('code.mem', 'w')  # redirect all prints to this code.mem file
    print(machinecode+'\n')  # nothing appears at interactive prompt
    sys.stdout.close()  # ordinary file object
    sys.stdout = temp  # restore print commands to interactive prompt

def main():
    me, fname = sys.argv

    f = open(fname, "r")
    labels = {}  # Map from label to its address.
    parsed_lines = []  # List of parsed instructions.
    address = 0  # Track the current address of the instruction.
    line_count = 0  # Number of lines.

    for line in f:
        line_list = []
        # Stores attributes about the current line of code, like its label, line
        # number, instruction, and arguments.
        line_attr = {}
        pattern = re.compile(r"\S[a-zA-Z0-9:$()#=\,]*")  # This is our pattern for seperating line into list of strings
        line_list = re.findall(pattern, line)  # This seperates a line into list of different strings

        if line:
            # We'll get you started here with line_count.
            line_attr['line_number'] = line_count
            comment_symbol = '#'
            comment = pluck_comment(comment_symbol, line_list)
            line_attr['comment'] = comment

            label_symbol = ':'
            line_attr, line_count = seperate_line_components(label_symbol, line_count, line_list, line_attr)
            # Handle comments, whitespace.
            # We'll get you started here with line_count.
            # Handle labels
            # Parse the rest of the instruction and its register arguments.

            # Finally, add this dict to the complete list of instructions.
            parsed_lines.append(line_attr)
    f.close()

    machine = ""  # Current machine code word.

    for line in parsed_lines:
        if line['instruction'] == 'nop':
            print(8 * '0')
        elif line['instruction'] in rtypes:
            op,rs,rt,rd,shamt,funct=r_instructions_components(line_attr,line)
            machinecode = op + rs + rt + rd + shamt + funct
            machinecode = bin_to_hex(machinecode)
            #print(line)
            write_file='code.mem'
            to_stdout(write_file,machinecode)
            print(machinecode)
            # sys.stdout.write(machinecode + '\n')
            # print(op)

            # Encode an R-type instruction.
        else:
            #print(line)
            op = op_codes[line['instruction']]
            try:
                if "(" in line['arg1']:
                    ind = line['arg1'].find('(')
                    imm = line['arg1'][:ind]
                    imm = dec_to_bin(imm, 16)
                    ind2 = line['arg1'].find(')')
                    arg1 = line['arg1'][ind + 1:ind2]
                    rs = registers[arg1]
                else:
                    imm = dec_to_bin(line['arg2'], 16)
                    rs = registers[line['arg1']]

                rt = registers[line['arg0']]
                machinecode = op + rs + rt + imm
                machinecode = bin_to_hex(machinecode)

                write_file = 'code.mem'
                to_stdout(write_file,machinecode)
                print(machinecode)
            except:
                print("problem")
                write_file = 'code.mem'
                to_stdout(write_file,machinecode)
            # sys.stdout.write(machinecode + '\n')
            # Encode a non-R-type instruction.

    return None


if __name__ == "__main__":
    main()
