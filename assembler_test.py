import unittest
from assembler import interpret, StateException


class TestAssembler(unittest.TestCase):
    def test_mov(self):
        # Test assigning constants or other register's values to a register, ints and floats
        register = interpret([
            'mov a, 5',
            'mov b, a',
            'mov c, 6.33',
            'mov d, c'
        ])
        self.assertEqual(register['a'], 5)
        self.assertEqual(register['b'], register['a'])
        self.assertEqual(register['c'], 6.33)
        self.assertEqual(register['d'], register['c'])

        with self.assertRaises(StateException):
            _ = interpret([
                'mov a, b, c'
            ])

        with self.assertRaises(StateException):
            _ = interpret([
                'mov a'
            ])

        # was fun, but not as fun as other things


if __name__ == '__main__':
    unittest.main()
