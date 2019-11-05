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
.. module: lycan.base
    :platform: Unix

.. version:: $$VERSION$$
.. moduleauthor:: Michael Stair <mstair@att.com>

"""

from stix2.base import _cls_init, _STIXBase, STIXJSONEncoder
from stix2.custom import _register_object
import copy
import itertools
import json
from collections import OrderedDict

class _OpenC2Base(_STIXBase):
    def serialize(self, pretty=False, **kwargs):
        if pretty:
            kwargs.update({'indent': 4, 'separators': (',', ': ')})
        return json.dumps(self, cls=OpenC2JSONEncoder, **kwargs)

class _OpenC2Type(_OpenC2Base):
    pass

class _Target(_OpenC2Base):
    def serialize(self, pretty=False, **kwargs):
        if pretty:
            kwargs.update({'indent': 4, 'separators': (',', ': ')})
        return json.dumps(self, cls=OpenC2JSONEncoder, **kwargs)

#targets with single specifiers 
class _SimpleTarget(_Target):
    pass

class _Actuator(_OpenC2Base):
    pass

class OpenC2JSONEncoder(STIXJSONEncoder):
    def default(self, obj):
        if isinstance(obj, _Target):
            tmp_obj = dict(copy.deepcopy(obj))
            #collapse targets that dont have object specifiers (ie, DomainName)
            if isinstance(obj, _SimpleTarget):
            #if len(obj._properties) == 1 and obj._type in obj._properties.keys():
                tmp_obj = tmp_obj.get(obj._type)
            return {obj._type:tmp_obj}
        else:
            return super(OpenC2JSONEncoder, self).default(obj)

def CustomOpenC2Object(type='x-custom-type', properties=None):
    def wrapper(cls):
        _properties = list(itertools.chain.from_iterable([
            [x for x in properties if not x[0].startswith('x_')],
            sorted([x for x in properties if x[0].startswith('x_')], key=lambda x: x[0]),
        ]))
        return _custom_object_builder(cls, type, _properties, '2.1')

    return wrapper


def _custom_object_builder(cls, type, properties, version):
    class _CustomOpenC2Object(cls, _OpenC2Base):

        #if not re.match(TYPE_REGEX, type):
        #    raise ValueError(
        #        "Invalid type name '%s': must only contain the "
        #        "characters a-z (lowercase ASCII), 0-9, and hyphen (-)." % type,
        #    )
        #elif len(type) < 3 or len(type) > 250:
        #    raise ValueError(
        #        "Invalid type name '%s': must be between 3 and 250 characters." % type,
        #    )

        if not properties or not isinstance(properties, list):
            raise ValueError("Must supply a list, containing tuples. For example, [('property1', IntegerProperty())]")

        _type = type
        _properties = OrderedDict(properties)

        def __init__(self, **kwargs):
            _OpenC2Base.__init__(self, **kwargs)
            _cls_init(cls, self, kwargs)

    _register_object(_CustomOpenC2Object, version=version)
    return _CustomOpenC2Object