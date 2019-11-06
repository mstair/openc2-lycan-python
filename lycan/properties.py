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
.. module: lycan.properties
    :platform: Unix

.. version:: $$VERSION$$
.. moduleauthor:: Michael Stair <mstair@att.com>

"""

from stix2 import properties
from stix2.properties import Property, DictionaryProperty
from stix2.utils import _get_dict
from .core import parse_target
from collections import OrderedDict

class PayloadProperty(Property):
    pass

HASHES_REGEX = {
    "MD5": (r"^[a-fA-F0-9]{32}$", "MD5"),
    "SHA1": (r"^[a-fA-F0-9]{40}$", "SHA-1"),
    "SHA256": (r"^[a-fA-F0-9]{64}$", "SHA-256"),
}

class HashesProperty(DictionaryProperty):

    def clean(self, value):
        clean_dict = super(HashesProperty, self).clean(value)
        for k, v in clean_dict.items():
            key = k.upper().replace('-', '')
            if key in HASHES_REGEX:
                vocab_key = HASHES_REGEX[key][1]
                if not re.match(HASHES_REGEX[key][0], v):
                    raise ValueError("'{0}' is not a valid {1} hash".format(v, vocab_key))
                if k != vocab_key:
                    clean_dict[vocab_key] = clean_dict[k]
                    del clean_dict[k]
        return clean_dict

class TargetProperty(Property):

    def __init__(self, allow_custom=False, *args, **kwargs):
        self.allow_custom = allow_custom
        super(TargetProperty, self).__init__(*args, **kwargs)

    def clean(self, value):
        dictified = {}
        try:
            #carry along the target type
            dictified[value._type]= _get_dict(value)
        except ValueError:
            raise ValueError("This property may only contain a dictionary or object")
        if dictified[value._type]== {}:
            raise ValueError("This property may only contain a non-empty dictionary or object")
        parsed_obj = parse_target(dictified, allow_custom=self.allow_custom)
        return parsed_obj