import math
from enum import Enum
import pycosat


def read_cnf_file(fname):
    # Parse a file in DIMACS .cnf format as described in the file
    # http://archive.dimacs.rutgers.edu/pub/challenge/satisfiability/doc/satformat.dvi
    #
    # A successfully parsed cnf results in a list of clauses where each clause is a list of positive and negative literals
    # described by positive and negative integers as in the DIMACS format. This list may be input directly to pycosat
    try:
        file = open(fname, 'r')
        lines = file.readlines()
        file.close()

        for c, line in enumerate(lines):
            if line[0] != 'c':
                break

        prob = lines[c].split()
        if len(prob) != 4 or prob[0] != 'p' or prob[1] != 'cnf':
            raise ValueError
        n = int(prob[2])
        m = int(prob[3])

        lits = [int(val) for val in (("".join(lines[(c + 1):])).split())]

        clauses = []
        clause = []
        for lit in lits:
            if lit == 0:
                clauses.append(clause)
                clause = []
            elif lit < -n or lit > n:
                raise ValueError
            else:
                clause.append(lit)
        if len(clauses) != m:
            raise ValueError
        return clauses
    except ValueError:
        return 'INVALID'


def write_cnf_file(cnf, fname, comments=["no description"]):
    # Write a cnf to the DIMACS .cnf format
    file = open(fname, 'w')
    for comment in comments:
        file.write('c ' + comment + '\n')
    m = len(cnf)
    lits = []
    for c in cnf:
        lits += c
    n = max(max(lits), -min(lits))
    file.write('p cnf {} {}\n'.format(n, m))
    for c in cnf:
        file.writelines((' '.join(map(str, c))) + ' 0\n')
    file.close()


gate_types = "01CANOEX"
nullary_gates = "01"
unary_gates = "CN"
binary_gates = "AOEX"


def valid_gate_type(g):
    return len(g) == 1 and gate_types.find(g) != -1


def is_nullary(g):
    return len(g) == 1 and nullary_gates.find(g) != -1


def is_unary(g):
    return len(g) == 1 and unary_gates.find(g) != -1


def is_binary(g):
    return len(g) == 1 and binary_gates.find(g) != -1


class Circuit:
    # A simple representation of a Boolean circuit

    # 'n' is an integer describing the number of inputs
    # 'gates' is a list of gates of the circuit. Each gate is a list of length 1, 2 or 3.
    # The i-th gate of the circuit is implicitly enumerated, starting from n+1.
    # The first element of each gate list is a character that specifies the type of gate
    # and the remaining elements are integers that specify the inputs to the gate
    # as described in the read_circuit_file function below.
    # The last gate of the circuit is the output of the circuit.

    def __init__(self, n, gates):
        self.n = n
        self.gates = gates

    def __str__(self):
        tmp = []
        for i, gate in enumerate(self.gates, self.n + 1):
            tmp.append('{} : {}\n'.format(i, gate))
        return ''.join(tmp)


def read_circuit_file(fname):
    # Parse a file in the Optimization .circuit format we define as follows:
    # The first line of file consists of a single number describing the number n of inputs to the circuit
    # Each remaining line describes a single gate of the circuit.
    # There must be at least one such line, and the last line describes the output gate of the circuit.
    # Gates are implicitly enumerated, starting from n+1. The inputs are numbered 1 through n.
    # A description of a gate consists of its type specified as a single character describing the type of function
    # followed by zero, one, or two postive integers (for nullary (i.e. constants), unary or binary gates).
    # A nullary gate is either the Boolean constant TRUE (type '1') or the Boolean constant FALSE (type '0').
    # A unary gate is either a COPY gate (type 'C') or a NOT gate (type 'N').
    # A binary gate is either an AND gate (type 'A'), an OR gate (type 'O'), an XOR gate (type 'X'), or an EQUAL gate (type 'E').
    # The input(s) to the gate is described by positive integers that may refer to either an input or to an *already described* gate.
    #
    # A successfully parsed circuit is returned as a Circuit class.
    # Otherwise the string 'INVALID' is returned.
    try:
        file = open(fname, 'r')
        lines = file.readlines()
        file.close()

        first_line = lines[0].split()
        if len(first_line) != 1:
            raise ValueError
        number_of_inputs = int(first_line[0])

        gates = [[character for character in line.split()] for line in lines[1:]]
        if len(gates) < 1:
            raise ValueError

        number_of_gates_already_described = number_of_inputs
        for gate_line in gates:
            if not valid_gate_type(gate_line[0]):
                raise ValueError
            elif is_nullary(gate_line[0]) and len(gate_line) != 1:
                raise ValueError
            elif is_unary(gate_line[0]) and (len(gate_line) != 2 or
                                             1 > int(gate_line[1]) > number_of_gates_already_described):
                raise ValueError
            elif is_binary(gate_line[0]) and (len(gate_line) != 3 or
                                              1 > int(gate_line[1]) > number_of_gates_already_described or
                                              1 > int(gate_line[2]) > number_of_gates_already_described):
                raise ValueError
            else:
                number_of_gates_already_described += 1

        return Circuit(number_of_inputs, gates)
    except ValueError:
        return 'INVALID'


def CSAT_gate_to_SAT_clause(y, gate):
    match gate[0]:
        case '0':
            return [[-y]]
        case '1':
            return [[y]]
        case 'A':
            return [[int(gate[1]), int(gate[2]), -y],
                    [int(gate[1]), -int(gate[2]), -y],
                    [-int(gate[1]), int(gate[2]), -y],
                    [-int(gate[1]), -int(gate[2]), y]]
        case 'O':
            return [[int(gate[1]), int(gate[2]), -y],
                    [int(gate[1]), -int(gate[2]), y],
                    [-int(gate[1]), int(gate[2]), y],
                    [-int(gate[1]), -int(gate[2]), y]]
        case 'N':
            return [[int(gate[1]), y],
                    [-int(gate[1]), -y]]
        case 'C':
            return [[int(gate[1]), -y],
                    [-int(gate[1]), y]]
        case 'X':
            return [[int(gate[1]), int(gate[2]), -y],
                    [int(gate[1]), -int(gate[2]), y],
                    [-int(gate[1]), int(gate[2]), y],
                    [-int(gate[1]), -int(gate[2]), -y]]
        case 'E':
            return [[int(gate[1]), int(gate[2]), y],
                    [int(gate[1]), -int(gate[2]), -y],
                    [-int(gate[1]), int(gate[2]), -y],
                    [-int(gate[1]), -int(gate[2]), y]]

def CSAT_to_SAT(C):
    # reduction between valid internal representations
    # input is a Circuit object
    # output is list of clauses that each are a list of positive and negative literals'
    # reduction has to be polynomial time and preserve (dis)satisfiability
    cnf = []
    for i, gate in enumerate(C.gates):
        y = C.n+1+i
        cnf.extend(CSAT_gate_to_SAT_clause(y, gate))
    cnf.append([y])
    return cnf


def reduce_CSAT_to_SAT(infile, outfile):
    # performs reduction from CircuitSAT to SAT
    # the input is read from infile and the output written to outfile
    # valid encodings of CSAT instances are encoded in the Optimization .circuit format
    # valid encodings of SAT instances are encoded in the DIMACS .cnf format
    c = read_circuit_file(infile)
    cnf = CSAT_to_SAT(c)
    write_cnf_file(cnf, outfile, ["Normal CircuitSAT reduced to SAT"])


def reduce_CSAT2_to_SAT(infile, outfile):
    # performs reduction from CircuitSAT2 to SAT
    # the input is read from infile and the output written to outfile
    # valid encodings of CSAT instances are encoded in the Optimization .circuit format
    # valid encodings of SAT instances are encoded in the DIMACS .cnf format
    c = read_circuit_file(infile)
    cnf_instance_one = CSAT_to_SAT(c)
    cnf_highest_numbered_literal = c.n + len(c.gates)
    cnf_instance_two = [[int(math.copysign(abs(lit)+cnf_highest_numbered_literal, lit)) for lit in clause] for clause in cnf_instance_one]
    next_gate_number = cnf_highest_numbered_literal * 2 + 1

    cnf_combined = []
    cnf_combined.extend(cnf_instance_one)
    cnf_combined.extend(cnf_instance_two)

    if c.n > 0:
        # Only accept when the assignment of the first instance is not equal to the assignment of the second instance
        first_equals_variable = next_gate_number
        for i in range(1, c.n+1):
            cnf_combined.extend(CSAT_gate_to_SAT_clause(next_gate_number, ['E', i, i+cnf_highest_numbered_literal]))
            next_gate_number += 1
        last_equals_variable = next_gate_number - 1
        number_of_equal_gates = last_equals_variable - first_equals_variable + 1
        if number_of_equal_gates > 1:
            # Add AND of all equal gates, and AND of all these AND gates, until only one output
            inputs = first_equals_variable
            while inputs < next_gate_number - 1:
                cnf_combined.extend(CSAT_gate_to_SAT_clause(next_gate_number, ['A', inputs, inputs+1]))
                next_gate_number += 1
                inputs += 2

        # Add NOT to last gate, to say that the sum of the equal-outputs should NOT be true
        cnf_combined.extend(CSAT_gate_to_SAT_clause(next_gate_number, ['N', next_gate_number - 1]))
        # Add that the output of the NOT-gate should be true
        cnf_combined.extend([[next_gate_number]])

    write_cnf_file(cnf_combined, outfile, ["CircuitSAT2 reduced to SAT"])
