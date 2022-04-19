from unittest import TestCase

import pycosat

from circuitsat import reduce_CSAT_to_SAT, read_cnf_file, reduce_CSAT2_to_SAT


class Test(TestCase):
    def test_or(self):
        reduce_CSAT_to_SAT('testfiles/or.circuit', 'testfiles/or.cnf')
        cnf = read_cnf_file('testfiles/or.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(True, res != 'UNSAT')

    def test_or2(self):
        reduce_CSAT2_to_SAT('testfiles/or.circuit', 'testfiles/or2.cnf')
        cnf = read_cnf_file('testfiles/or2.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(True, res != 'UNSAT')

    def test_and(self):
        reduce_CSAT_to_SAT('testfiles/and.circuit', 'testfiles/and.cnf')
        cnf = read_cnf_file('testfiles/and.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(True, res != 'UNSAT')

    def test_and2(self):
        reduce_CSAT2_to_SAT('testfiles/and.circuit', 'testfiles/and2.cnf')
        cnf = read_cnf_file('testfiles/and2.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(False, res != 'UNSAT')

    def test_equal(self):
        reduce_CSAT_to_SAT('testfiles/equal.circuit', 'testfiles/equal.cnf')
        cnf = read_cnf_file('testfiles/equal.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(True, res != 'UNSAT')

    def test_equal2(self):
        reduce_CSAT2_to_SAT('testfiles/equal.circuit', 'testfiles/equal2.cnf')
        cnf = read_cnf_file('testfiles/equal2.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(True, res != 'UNSAT')

    def test_xor(self):
        reduce_CSAT_to_SAT('testfiles/xor.circuit', 'testfiles/xor.cnf')
        cnf = read_cnf_file('testfiles/xor.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(True, res != 'UNSAT')

    def test_xor2(self):
        reduce_CSAT2_to_SAT('testfiles/xor.circuit', 'testfiles/xor2.cnf')
        cnf = read_cnf_file('testfiles/xor2.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(True, res != 'UNSAT')

    def test_not(self):
        reduce_CSAT_to_SAT('testfiles/not.circuit', 'testfiles/not.cnf')
        cnf = read_cnf_file('testfiles/not.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(True, res != 'UNSAT')

    def test_not2(self):
        reduce_CSAT2_to_SAT('testfiles/not.circuit', 'testfiles/not2.cnf')
        cnf = read_cnf_file('testfiles/not2.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(False, res != 'UNSAT')

    def test_copy(self):
        reduce_CSAT_to_SAT('testfiles/copy.circuit', 'testfiles/copy.cnf')
        cnf = read_cnf_file('testfiles/copy.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(True, res != 'UNSAT')

    def test_copy2(self):
        reduce_CSAT2_to_SAT('testfiles/copy.circuit', 'testfiles/copy2.cnf')
        cnf = read_cnf_file('testfiles/copy2.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(False, res != 'UNSAT')

    def test_true(self):
        reduce_CSAT_to_SAT('testfiles/true.circuit', 'testfiles/true.cnf')
        cnf = read_cnf_file('testfiles/true.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(True, res != 'UNSAT')

    def test_true2(self):
        reduce_CSAT2_to_SAT('testfiles/true.circuit', 'testfiles/true2.cnf')
        cnf = read_cnf_file('testfiles/true2.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(True, res != 'UNSAT')

    def test_false(self):
        reduce_CSAT_to_SAT('testfiles/false.circuit', 'testfiles/false.cnf')
        cnf = read_cnf_file('testfiles/false.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(res != 'UNSAT', False)

    def test_false2(self):
        reduce_CSAT2_to_SAT('testfiles/false.circuit', 'testfiles/false2.cnf')
        cnf = read_cnf_file('testfiles/false2.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(res != 'UNSAT', False)

    def test_test1p(self):
        reduce_CSAT_to_SAT('testfiles/test1p.circuit', 'testfiles/test1p.cnf')
        cnf = read_cnf_file('testfiles/test1p.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(True, res != 'UNSAT')

    def test_test1p2(self):
        reduce_CSAT2_to_SAT('testfiles/test1p.circuit', 'testfiles/test1p2.cnf')
        cnf = read_cnf_file('testfiles/test1p2.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(True, res != 'UNSAT')

    def test_false_and(self):
        reduce_CSAT_to_SAT('testfiles/false_and.circuit', 'testfiles/false_and.cnf')
        cnf = read_cnf_file('testfiles/false_and.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(False, res != 'UNSAT')

    def test_false_and2(self):
        reduce_CSAT2_to_SAT('testfiles/false_and.circuit', 'testfiles/false_and.cnf')
        cnf = read_cnf_file('testfiles/false_and.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(False, res != 'UNSAT')

    def test_false_or(self):
        reduce_CSAT_to_SAT('testfiles/false_or.circuit', 'testfiles/false_or.cnf')
        cnf = read_cnf_file('testfiles/false_or.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(True, res != 'UNSAT')

    def test_false_or2(self):
        reduce_CSAT2_to_SAT('testfiles/false_or.circuit', 'testfiles/false_or.cnf')
        cnf = read_cnf_file('testfiles/false_or.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(False, res != 'UNSAT')

    def test_div1(self):
        reduce_CSAT_to_SAT('div1.circuit', 'div1.cnf')
        cnf = read_cnf_file('div1.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(True, res != 'UNSAT')

    def test_div2(self):
        reduce_CSAT_to_SAT('div2.circuit', 'div2.cnf')
        cnf = read_cnf_file('div2.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(False, res != 'UNSAT')

    def test_sub1(self):
        reduce_CSAT_to_SAT('sub1.circuit', 'sub1.cnf')
        cnf = read_cnf_file('sub1.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(True, res != 'UNSAT')

    def test_sub2(self):
        reduce_CSAT_to_SAT('sub2.circuit', 'sub2.cnf')
        cnf = read_cnf_file('sub2.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(True, res != 'UNSAT')

    def test_test1(self):
        reduce_CSAT_to_SAT('test1.circuit', 'test1.cnf')
        cnf = read_cnf_file('test1.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(False, res != 'UNSAT')

    def test_test2(self):
        reduce_CSAT_to_SAT('test2.circuit', 'test2.cnf')
        cnf = read_cnf_file('test2.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(True, res != 'UNSAT')

    def test_hanoi4(self):
        cnf = read_cnf_file('hanoi4.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(True, res != 'UNSAT')

    def test_hole6(self):
        cnf = read_cnf_file('hole6.cnf')
        res = pycosat.solve(cnf)
        self.assertEqual(False, res != 'UNSAT')
