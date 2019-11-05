from lycan.message import Command, Response

from .targets import (
    Artifact, Device, DomainName, EmailAddress, Features, File,
    InternationalizedDomainName, InternationalizedEmailAddress, IPv4AddressRange,
    IPv6AddressRange, IPv4Connection, IPv6Connection, IRI, MacAddress, Process,
    Properties, URI
)

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
    'ipv4_net': IPv4AddressRange,
    'ipv6_net': IPv6AddressRange,
    'ipv4_connection': IPv4Connection,
    'ipv6_connection': IPv6Connection,
    'iri': IRI,
    'mac_addr': MacAddress,
    'process': Process,
    'properties': Properties,
    'uri': URI
}

