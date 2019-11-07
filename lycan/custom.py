from collections import OrderedDict

from stix2.base import _cls_init
from .base import _OpenC2Base, _Target, _Actuator
from .core import OPENC2_OBJ_MAPS

def _register_extension(new_type, object_type=None, version=None):
    #if not object_type:
        #raise

    EXT_MAP = OPENC2_OBJ_MAPS['extensions']
    EXT_MAP[object_type][new_type._type] = new_type

def _custom_target_builder(cls, type, properties, version):
    class _CustomTarget(cls, _Target):

        try:
            nsid, target = type.split(':')
        except IndexError:
            raise ValueError(
                "Invalid Extended Target name '%s': must be namespace:target format" % type
            )
        if len(nsid) > 16:
            raise ValueError(
                "Invalid namespace '%s': must be less than 16 characters" % type
            )

        if not properties or not isinstance(properties, list):
            raise ValueError("Must supply a list, containing tuples. For example, [('property1', IntegerProperty())]")

        _type = type
        _properties = OrderedDict(properties)

        def __init__(self, **kwargs):
            _Target.__init__(self, **kwargs)
            _cls_init(cls, self, kwargs)

    _register_extension(_CustomTarget, object_type="targets", version=version)
    return _CustomTarget


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

    _register_extension(_CustomActuator, object_type="actuators", version=version)
    return _CustomActuator

def _custom_args_extension_builder(cls, type, properties, version):
    class _CustomArgsExtension(cls, _OpenC2Base):

        if not properties or not isinstance(properties, list):
            raise ValueError("Must supply a list, containing tuples. For example, [('property1', IntegerProperty())]")

        _type = type
        _properties = OrderedDict(properties)

        def __init__(self, **kwargs):
            _OpenC2Base.__init__(self, **kwargs)
            _cls_init(cls, self, kwargs)

    _register_extension(_CustomArgsExtension, object_type="args", version=version)
    return _CustomArgsExtension