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

import unittest,json
import lycan.datamodels as openc2
from lycan.message import OpenC2Command, OpenC2Response, OpenC2Target, OpenC2Actuator
from lycan.serializations import OpenC2MessageDecoder

class TestJsonDecode(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_command_decode(self):
        _msg = {
               'action': 'deny',
			   'target': {
                   'ipv4_net': '1.2.3.4'
               },
               'actuator': {
                   'network_firewall': {
                   }
               },
               'args': {
                   'foo': 'bar'
               }
        }
        cmd = OpenC2MessageDecoder().decode(json.dumps(_msg))
        self.assertEqual(cmd.action, 'deny')
        _msg = {
               'action':'locate',
               'target': {
                   'file': {
                       'name': 'passwd',
                       'hashes': '0x129823'
                   }
               },
               'args': {
                   'foo': 'bar'
               }
        }
        cmd = OpenC2MessageDecoder().decode(json.dumps(_msg))
        self.assertEqual(cmd.target.name, 'passwd')

    def test_command_decode_invalid(self):
        _msg = {
               'action':'deny',
        }
        cmd = OpenC2MessageDecoder()
        self.assertRaises(ValueError, cmd.decode, json.dumps(_msg))

    def test_response_decode(self):
        _msg = {
               'status': 200,
               'status_text':'passed',
               'results':'foo'
        }
        response = OpenC2MessageDecoder().decode(json.dumps(_msg))
        self.assertEqual(response.status, 200)
