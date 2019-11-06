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

import copy
import json

class OpenC2JSONEncoder(STIXJSONEncoder):
    def default(self, obj):
        if isinstance(obj, (_Target, _Actuator)):
            tmp_obj = dict(copy.deepcopy(obj))
            #collapse targets with a single specifier (ie, DomainName)
            if len(obj._properties) == 1 and obj._type in obj._properties.keys():
                tmp_obj = tmp_obj.get(obj._type)
            return {obj._type:tmp_obj}
        else:
            return super(OpenC2JSONEncoder, self).default(obj)

class _OpenC2Base(_STIXBase):
    def serialize(self, pretty=False, **kwargs):
        if pretty:
            kwargs.update({'indent': 4, 'separators': (',', ': ')})
        return json.dumps(self, cls=OpenC2JSONEncoder, **kwargs)

class _OpenC2DataType(_OpenC2Base):
    pass

class _Target(_OpenC2Base):
    pass

class _Actuator(_OpenC2Base):
    pass