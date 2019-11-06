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

"""
.. module: lycan.targets
    :platform: Unix

.. version:: $$VERSION$$
.. moduleauthor:: Michael Stair <mstair@att.com>

"""

from stix2 import properties
from lycan.properties import PayloadProperty
from lycan.base import _Target
from lycan.custom import _custom_target_builder

import itertools
from collections import OrderedDict

class Artifact(_Target):
    _type = 'artifact'
    _properties = OrderedDict([
        ('mime_type', properties.StringProperty()),
        ('payload', PayloadProperty()),
        ('hashes', properties.HashesProperty()),
    ])

    def _check_object_constraints(self):
        super(Artifact, self)._check_object_constraints()
        self._check_mutually_exclusive_properties(['payload', 'url'])

class Device(_Target):
    _type = 'device'
    _properties = OrderedDict([
        ('hostname', properties.StringProperty()),
        ('idn_hostname', properties.StringProperty()),
        ('device_id', properties.StringProperty())
    ])

class DomainName(_Target):
    _type = 'domain_name'
    _properties = OrderedDict([
        ('domain_name', properties.StringProperty(required=True)),
    ])

class EmailAddress(_Target):
    _type = 'email_addr'
    _properties = OrderedDict([
        ('email_addr', properties.StringProperty(required=True)),
    ])

class Features(_Target): 
    _type = 'features'
    _properties = OrderedDict([
        ('features', properties.ListProperty(properties.StringProperty))
    ])
#    def __init__(self, features=None, **kwargs):
#        if len(features) > 10:
#            raise ValueError("Maximum of 10 features allowed")
#        for feature in features:
#            #check for x-
#            if feature not in ["versions", "profiles", "pairs", "rate_limit"]:
#                raise ValueError("%s is an unsupported feature")

class File(_Target): 
    _type = 'file'
    _properties = OrderedDict([
        ('name', properties.StringProperty()),
        ('path', properties.StringProperty()),
        ('hashes', properties.HashesProperty())
    ])

class InternationalizedDomainName(_Target):
    _type = 'idn_domain_name'
    _properties = OrderedDict([
        ('idn_domain_name', properties.StringProperty(required=True)),
    ])

class InternationalizedEmailAddress(_Target):
    _type = 'idn_email'
    _properties = OrderedDict([
        ('idn_email', properties.StringProperty(required=True)),
    ])

class IPv4AddressRange(_Target):
    _type = 'ipv4_net'
    _properties = OrderedDict([
        ('ipv4_net', properties.StringProperty(required=True)),
    ])

class IPv6AddressRange(_Target):
    _type = 'ipv6_net'
    _properties = OrderedDict([
        ('ipv6_net', properties.StringProperty(required=True)),
    ])

class IPv4Connection(_Target):
    _type = 'ipv4_connection'
    _properties = OrderedDict([
        ('src_addr', properties.StringProperty()),
        ('src_port', properties.IntegerProperty(min=0, max=65535)),
        ('dst_addr', properties.StringProperty()),
        ('dst_port', properties.IntegerProperty(min=0, max=65535)),
        ('protocol', properties.EnumProperty(
            allowed=[
                "icmp",
                "tcp",
                "udp",
                "sctp"
            ]
        ))
    ])

class IPv6Connection(_Target):
    _type = 'ipv6_connection'
    _properties = OrderedDict([
        ('src_addr', properties.StringProperty()),
        ('src_port', properties.IntegerProperty(min=0, max=65535)),
        ('dst_addr', properties.StringProperty()),
        ('dst_port', properties.IntegerProperty(min=0, max=65535)),
        ('protocol', properties.EnumProperty(
            allowed=[
                "icmp",
                "tcp",
                "udp",
                "sctp"
            ]
        ))
    ])
#    def __init__(self, src_port=None, dst_port=None, **kwargs):
#        if src_port and (src_port < 0 or src_port > 65535):
#            raise ValueError("invalid src_port")
#        if dst_port and (dst_port < 0 or dst_port > 65535):
#            raise ValueError("invalid dst_port")

class IRI(_Target):
    _type = 'iri'
    _properties = OrderedDict([
        ('iri', properties.StringProperty(required=True)),
    ])

class MacAddress(_Target):
    _type = 'mac_addr'
    _properties = OrderedDict([
        ('mac_addr', properties.StringProperty(required=True)),
    ])

class Process(_Target):
    _type = 'process'
    _properties = OrderedDict([
        ('pid', properties.StringProperty()),
        ('name', properties.StringProperty()),
        ('cmd', properties.StringProperty()),
        ('executable', properties.StringProperty()),
        ('parent', properties.StringProperty()), #handle parent process
        ('command_line', properties.StringProperty()),
    ])

class Properties(_Target):
    _type = 'properties'
    _properties = OrderedDict([
        ('properties', properties.StringProperty(required=True)),
    ])

class URI(_Target):
    _type = 'uri'
    _properties = OrderedDict([
        ('uri', properties.StringProperty(required=True)),
    ])

def CustomTarget(type='x-acme', properties=None):
    def wrapper(cls):
        _properties = list(itertools.chain.from_iterable([
            [x for x in properties if not x[0].startswith('x_')],
            sorted([x for x in properties if x[0].startswith('x_')], key=lambda x: x[0]),
        ]))
        return _custom_target_builder(cls, type, _properties, '2.1')

    return wrapper