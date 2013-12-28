import unittest

from construct import ByteRange, Struct, UBInt8
# TODO python3

class TestByteRange(unittest.TestCase):
    def setUp(self):
        self.br = ByteRange('br', 3, 7)

    def test_parse(self):
        self.assertEqual(self.br.parse('abc'), 'abc')
        self.assertEqual(self.br.parse('abcde'), 'abcde')
        self.assertEqual(self.br.parse('abcdefg'), 'abcdefg')
        self.assertEqual(self.br.parse('abcdefghi'), 'abcdefg')

    def test_parse_rest(self):
        c = Struct('foo', self.br, UBInt8('bar'))

        self.assertEqual(c.parse('abcdefg' + chr(42))['bar'], 42)

    def test_build(self):
        self.assertEqual(self.br.build('abc'), 'abc')
        self.assertEqual(self.br.parse('abcde'), 'abcde')
        self.assertEqual(self.br.parse('abcdefg'), 'abcdefg')

    def test_parse_too_short(self):
        self.assertRaises(Exception, self.br.parse, 'ab')
        self.assertRaises(Exception, self.br.parse, '')

    def test_build_too_short(self):
        self.assertRaises(Exception, self.br.build, '')
        self.assertRaises(Exception, self.br.build, 'ab')

    def test_build_too_long(self):
        self.assertRaises(Exception, self.br.build, 'abcdefgh')
