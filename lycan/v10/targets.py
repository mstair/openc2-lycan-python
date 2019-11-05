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
from lycan.base import CustomOpenC2Object, _Target, _SimpleTarget

from collections import OrderedDict

@CustomOpenC2Object('artifact', [
    ('mime_type', properties.StringProperty()),
    ('payload', PayloadProperty()),
    ('hashes', properties.HashesProperty()),
])
class Artifact(_Target):
    def _check_object_constraints(self):
        super(Artifact, self)._check_object_constraints()
        self._check_mutually_exclusive_properties(['payload', 'url'])

@CustomOpenC2Object('device', [
    ('hostname', properties.StringProperty()),
    ('idn_hostname', properties.StringProperty()),
    ('device_id', properties.StringProperty())
])
class Device(_Target):
    pass

@CustomOpenC2Object('domain_name', [
    ('domain_name', properties.StringProperty(required=True)),
])
class DomainName(_SimpleTarget):
    pass

@CustomOpenC2Object('email_addr', [
    ('email_addr', properties.StringProperty(required=True)),
])
class EmailAddress(_Target):
    pass

@CustomOpenC2Object('features', [
    ('features', properties.ListProperty(properties.StringProperty))
])
class Features(_Target): 
    def __init__(self, features=None, **kwargs):
        if len(features) > 10:
            raise ValueError("Maximum of 10 features allowed")
        for feature in features:
            #check for x-
            if feature not in ["versions", "profiles", "pairs", "rate_limit"]:
                raise ValueError("%s is an unsupported feature")

@CustomOpenC2Object('file', [
    ('name', properties.StringProperty()),
    ('path', properties.StringProperty()),
    ('hashes', properties.HashesProperty())
])
class File(_Target): 
    pass

@CustomOpenC2Object('idn_domain_name', [
    ('idn_domain_name', properties.StringProperty(required=True)),
])
class InternationalizedDomainName(_Target):
    pass

@CustomOpenC2Object('idn_email', [
    ('idn_email', properties.StringProperty(required=True)),
])
class InternationalizedEmailAddress(_Target):
    pass

@CustomOpenC2Object('ipv4_net', [
    ('ipv4_net', properties.StringProperty(required=True)),
])
class IPv4AddressRange(_Target):
    pass

@CustomOpenC2Object('ipv6_net', [
    ('ipv6_net', properties.StringProperty(required=True)),
])
class IPv6AddressRange(_Target):
    pass

#@CustomOpenC2Object('ipv4_connection', [
#    ('src_addr', properties.StringProperty()),
#    ('src_port', properties.StringProperty()),
#    ('dst_addr', properties.StringProperty()),
#    ('dst_port', properties.StringProperty()),
#    ('protocol', properties.EnumProperty(
#        allowed=[
#            "icmp",
#            "tcp",
#            "udp",
#            "sctp"
#        ]
#    ))
#])
#class IPv4Connection(_Target):
#    pass
#    def __init__(self, src_port=None, dst_port=None, **kwargs):
#        if src_port and (src_port < 0 or src_port > 65535):
#            raise ValueError("invalid src_port")
#        if dst_port and (dst_port < 0 or dst_port > 65535):
#            raise ValueError("invalid dst_port")
class IPv4Connection(_Target):
    _type = 'ipv4_connection'
    _properties = OrderedDict([
    ('src_addr', properties.StringProperty()),
    ('src_port', properties.StringProperty()),
    ('dst_addr', properties.StringProperty()),
    ('dst_port', properties.StringProperty()),
    ('protocol', properties.EnumProperty(
        allowed=[
            "icmp",
            "tcp",
            "udp",
            "sctp"
        ]
    ))
    ])

    def __init__(self, allow_custom=False, **kwargs):
        super(IPv4Connection,self).__init__(allow_custom=False, **kwargs)
        self._collapse = True

@CustomOpenC2Object('ipv6_connection', [
    ('src_addr', properties.StringProperty()),
    ('src_port', properties.StringProperty()),
    ('dst_addr', properties.StringProperty()),
    ('dst_port', properties.StringProperty()),
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
    def __init__(self, src_port=None, dst_port=None, **kwargs):
        if src_port and (src_port < 0 or src_port > 65535):
            raise ValueError("invalid src_port")
        if dst_port and (dst_port < 0 or dst_port > 65535):
            raise ValueError("invalid dst_port")

@CustomOpenC2Object('iri', [
    ('iri', properties.StringProperty(required=True)),
])
class IRI(_Target):
    pass

@CustomOpenC2Object('mac_addr', [
    ('mac_addr', properties.StringProperty(required=True)),
])
class MacAddress(_Target):
    pass

@CustomOpenC2Object('process', [
    ('pid', properties.StringProperty()),
    ('name', properties.StringProperty()),
    ('cmd', properties.StringProperty()),
    ('executable', properties.StringProperty()),
    ('executable', properties.StringProperty()),
    ('parent', properties.StringProperty()),
    ('command_line', properties.StringProperty()),
])
class Process(_Target):
    #handle parent process
    pass

@CustomOpenC2Object('properties', [
    ('properties', properties.StringProperty(required=True)),
])
class Properties(_Target):
    pass

@CustomOpenC2Object('uri', [
    ('uri', properties.StringProperty(required=True)),
])
class URI(_Target):
    pass