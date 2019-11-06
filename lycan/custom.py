from collections import OrderedDict

from stix2.base import _cls_init
from .base import _OpenC2Base, _Target, _Actuator
from stix2.custom import _register_object

def _custom_target_builder(cls, type, properties, version):
    class _CustomTarget(cls, _Target):

        if not ':' in type:
            raise ValueError(
                "Invalid Extended Target name '%s': must contain a colon" % type
            )

        if not properties or not isinstance(properties, list):
            raise ValueError("Must supply a list, containing tuples. For example, [('property1', IntegerProperty())]")

        _type = type
        _properties = OrderedDict(properties)

        def __init__(self, **kwargs):
            _Target.__init__(self, **kwargs)
            _cls_init(cls, self, kwargs)

    _register_object(__CustomTarget, version=version)
    return __CustomTarget


def _custom_actuator_builder(cls, type, properties, version):
    class _CustomActuator(cls, _Actuator):

        if not type.startswith('x-'):
            raise ValueError(
                "Invalid Extended Actuator name '%s': must start with x-" % type
            )

        if not properties or not isinstance(properties, list):
            raise ValueError("Must supply a list, containing tuples. For example, [('property1', IntegerProperty())]")

        _type = type
        _properties = OrderedDict(properties)

        def __init__(self, **kwargs):
            _Actuator.__init__(self, **kwargs)
            _cls_init(cls, self, kwargs)

    _register_object(_CustomActuator, version=version)
    return _CustomActuator
