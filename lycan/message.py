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
.. module: lycan.message
    :platform: Unix

.. version:: $$VERSION$$
.. moduleauthor:: Michael Stair <mstair@att.com>

"""

from lycan import __version__, OpenC2CommandField, OpenC2Specifiers
from munch import Munch, DefaultFactoryMunch
import six

OpenC2Args = OpenC2Specifiers

class OpenC2Target(OpenC2CommandField):
    """Class for OpenC2 Target

    Attributes:
        _name(str): The name of the object of the action
        _specifiers(str, dict, Munch): Further identifies the target
             to some level of precision, such as a specific target,
             a list of targets, or a class of targets.
    """
    def __init__(self, _name, *args, **kwargs):
        super(OpenC2Target, self).__init__(_name)
        self._specifiers = OpenC2Specifiers(kwargs)
        if args and len(args) == 1 and isinstance(args[0], six.string_types):
            self._specifiers = args[0]

class OpenC2Actuator(OpenC2CommandField):
    """Class for OpenC2 Actuator

    Attributes:
        _name(str): The name of the set of functions performed by
            the actuator, and the name of the profile defining
            commands applicable to those functions.
        _specifiers(dict, Munch): The specifier identifies the
            actuator to some level of precision, such as a
            specific actuator, a list of actuators, or a group of
            actuators.
    """
    def __init__(self, _name, **kwargs):
        super(OpenC2Actuator, self).__init__(_name)
        self._specifiers = OpenC2Specifiers(kwargs)

class OpenC2Command(object):
    """Class for OpenC2 Command

    Attributes:
        action (str): The task or activity to be performed
        target (OpenC2Target): The object of the action. The action is
            performed on the target.
        args (OpenC2Args, dict, Munch, optional): Identifier
            used to link responses to a command
        actuator (OpenC2Actuator, optional): An object containing
            additional properties that apply to the command
        command_id (str, optional): An identifier of this command
    Raises:
        ValueError: If missing any required fields
    """
    def __init__(self, action, target, args={}, actuator=None, command_id=None):
        super(OpenC2Command, self).__init__()
        self.action = action
        self.target = target
        self.args = OpenC2Specifiers(args)
        self.actuator = actuator
        self.command_id = command_id
        self.validate()

    def validate(self):
        #todo: validate each field against json schema
        #https://github.com/bberliner/openc2-json-schema/tree/master/src/main/resources
        return

class OpenC2Response(object):
    """Class for OpenC2 Response

    Attributes:
        status (int): An integer status code
        status_text (str, optional): A free-form human-readable
            description of the response status
        results (str, optional): Data or extended status information
            that was requested from an OpenC2 Command
    """
    def __init__(self, status, status_text=None, results=None):
        super(OpenC2Response, self).__init__()
        self.status = status
        self.status_text = status_text
        self.results = results
        self.validate()

    def validate(self):
        #todo: validate each field against json schema
        #https://github.com/bberliner/openc2-json-schema/tree/master/src/main/resources
        return