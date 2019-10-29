#
#  The MIT License (MIT)
#
# Copyright 2019 AT&T Intellectual Property. All other rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
# AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import unittest
from lycan.message import OpenC2CommandField, OpenC2Command, OpenC2Target, OpenC2Actuator

class TestOpenC2CommandField(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_init_str(self):
        x = OpenC2CommandField('foo')
        self.assertEqual(x, 'foo')
    def test_init_dict(self):
        x = OpenC2CommandField('foo')
        self.assertEqual(x, 'foo')
    def test_specifier_set(self):
        x = OpenC2CommandField('foo')
        x.value = 1
        self.assertEqual(x.value, 1)
    def test_specifiers_get(self):
        x = OpenC2CommandField('foo')
        self.assertEqual(x.specifiers, None)

class TestOpenC2Command(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_init_fail(self):
        self.assertRaises(TypeError, OpenC2Command, 'deny')
    def test_init_noactuator(self):
        x = OpenC2Command('deny', OpenC2Target('ipv4_net'))
        self.assertEqual(x.action, 'deny')
    def test_init_actuator(self):
        x = OpenC2Command('deny', OpenC2Target('ipv4_net'), {'han':'yah'}, OpenC2Actuator('slpf'))
        self.assertEqual(x.actuator, 'slpf')
    def test_init_args(self):
        x = OpenC2Command('deny', OpenC2Target('ipv4_net'), {'foo':'bar'}, OpenC2Actuator('slpf'))
        self.assertEqual(x.args.foo, 'bar')

class TestOpenC2Actuator(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_init_version(self):
        x = OpenC2Actuator('firewall', where='perimeter', asset_id='123')
        self.assertEqual(x, 'firewall')
