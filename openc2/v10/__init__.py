from .message import Command, Response

from .targets import (
    Artifact, Device, DomainName, EmailAddress, Features, File,
    InternationalizedDomainName, InternationalizedEmailAddress, IPv4Address,
    IPv6Address, IPv4Connection, IPv6Connection, IRI, MACAddress, Process,
    Properties, URI, CustomTarget
)

from .common import Payload

from .args import Args, CustomArgs

from .actuators import SLPF, CustomActuator

OBJ_MAP = {
    'command': Command,
    'response': Response
}

OBJ_MAP_TARGET = {
    'artifact': Artifact,
    'device': Device,
    'domain_name': DomainName,
    'email_addr': EmailAddress,
    'features': Features,
    'file': File,
    'idn_domain_name': InternationalizedDomainName,
    'idn_email': InternationalizedEmailAddress,
    'ipv4_net': IPv4Address,
    'ipv6_net': IPv6Address,
    'ipv4_connection': IPv4Connection,
    'ipv6_connection': IPv6Connection,
    'iri': IRI,
    'mac_addr': MACAddress,
    'process': Process,
    'properties': Properties,
    'uri': URI
}

OBJ_MAP_ACTUATOR = {
    'slpf': SLPF
}

OBJ_MAP_ARGS = {
    'args': Args
}

EXT_MAP = {
    'targets': {},
    'actuators': {},
    'args': {}
}
