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

from stix2.utils import _get_dict
from stix2.exceptions import CustomContentError, ParseError

import copy
import importlib
import pkgutil
import re

OPENC2_OBJ_MAPS = {}

def parse(data, allow_custom=False, version=None):
    """Convert a string, dict or file-like object into a OpenC2 object.

    Args:
        data (str, dict, file-like object): The STIX 2 content to be parsed.
        allow_custom (bool): Whether to allow custom properties as well unknown
            custom objects. Note that unknown custom objects cannot be parsed
            into STIX objects, and will be returned as is. Default: False.
        version (str): If present, it forces the parser to use the version
            provided. Otherwise, the library will make the best effort based
            on checking the "spec_version" property. If none of the above are
            possible, it will use the default version specified by the library.

    Returns:
        An instantiated Python STIX object.

    Warnings:
        'allow_custom=True' will allow for the return of any supplied STIX
        dict(s) that cannot be found to map to any known STIX object types
        (both STIX2 domain objects or defined custom STIX2 objects); NO
        validation is done. This is done to allow the processing of possibly
        unknown custom STIX objects (example scenario: I need to query a
        third-party TAXII endpoint that could provide custom STIX objects that
        I don't know about ahead of time)

    """
    # convert STIX object to dict, if not already
    obj = _get_dict(data)
    # convert dict to full python-stix2 obj
    obj = dict_to_openc2(obj, allow_custom, version)

    return obj


def dict_to_openc2(openc2_dict, allow_custom=False, version=None):
    """convert dictionary to full python-stix2 object

    Args:
        stix_dict (dict): a python dictionary of a STIX object
            that (presumably) is semantically correct to be parsed
            into a full python-stix2 obj
        allow_custom (bool): Whether to allow custom properties as well
            unknown custom objects. Note that unknown custom objects cannot
            be parsed into STIX objects, and will be returned as is.
            Default: False.
        version (str): If present, it forces the parser to use the version
            provided. Otherwise, the library will make the best effort based
            on checking the "spec_version" property. If none of the above are
            possible, it will use the default version specified by the library.

    Returns:
        An instantiated Python STIX object

    Warnings:
        'allow_custom=True' will allow for the return of any supplied STIX
        dict(s) that cannot be found to map to any known STIX object types
        (both STIX2 domain objects or defined custom STIX2 objects); NO
        validation is done. This is done to allow the processing of
        possibly unknown custom STIX objects (example scenario: I need to
        query a third-party TAXII endpoint that could provide custom STIX
        objects that I don't know about ahead of time)

    """
    message_type = None
    if 'action' in openc2_dict:
        message_type = 'command'
    elif 'status' in openc2_dict:
        message_type = 'response'
    else:
        raise ParseError("Can't parse object that is not valid command or response: %s" % str(openc2_dict))

    OBJ_MAP = OPENC2_OBJ_MAPS['objects']

    try:
        obj_class = OBJ_MAP[message_type]
    except KeyError:
        if allow_custom:
            # flag allows for unknown custom objects too, but will not
            # be parsed into STIX object, returned as is
            return openc2_dict
        raise ParseError("Can't parse unknown object type '%s'! For custom types, use the CustomObject decorator." % openc2_dict['type'])

    return obj_class(allow_custom=allow_custom, **openc2_dict)


def parse_target(data, allow_custom=False, version=None):
    """Deserialize a string or file-like object into a STIX Cyber Observable
    object.

    Args:
        data (str, dict, file-like object): The STIX2 content to be parsed.
        _valid_refs: A list of object references valid for the scope of the
            object being parsed. Use empty list if no valid refs are present.
        allow_custom (bool): Whether to allow custom properties or not.
            Default: False.
        version (str): If present, it forces the parser to use the version
            provided. Otherwise, the default version specified by the library
            will be used.

    Returns:
        An instantiated Python STIX Cyber Observable object.

    """
    obj = _get_dict(data)
    # modify the original dict as _get_dict() does not return new
    # dict when passed a dict
    obj = copy.deepcopy(obj)

    target_type = list(obj.keys())[0]
    target_specifiers = list(obj.values())[0]

    try:
        OBJ_MAP_TARGET = OPENC2_OBJ_MAPS['targets']
        obj_class = OBJ_MAP_TARGET[target_type]
    except KeyError:
        if allow_custom:
            # flag allows for unknown custom objects too, but will not
            # be parsed into STIX observable object, just returned as is
            return obj
        raise CustomContentError("Can't parse unknown observable type '%s'! For custom observables, "
                                 "use the CustomObservable decorator." % target_type)

    #handle targets with single value specifiers
    if isinstance(target_specifiers, dict):
        obj = obj[target_type]

    return obj_class(allow_custom=allow_custom, **obj)


def _collect_openc2_mappings():
    """Navigate the package once and retrieve all object mapping dicts for each
    v2X package. Includes OBJ_MAP, OBJ_MAP_OBSERVABLE, EXT_MAP."""
    if not OPENC2_OBJ_MAPS:
        top_level_module = importlib.import_module('lycan')
        path = top_level_module.__path__
        prefix = str(top_level_module.__name__) + '.'

        for module_loader, name, is_pkg in pkgutil.walk_packages(path=path, prefix=prefix):
            ver = name.split('.')[1]
            if re.match(r'^lycan\.v1[0-9]$', name) and is_pkg:
                mod = importlib.import_module(name, str(top_level_module.__name__))
                OPENC2_OBJ_MAPS['objects'] = mod.OBJ_MAP
                OPENC2_OBJ_MAPS['targets'] = mod.OBJ_MAP_TARGET
