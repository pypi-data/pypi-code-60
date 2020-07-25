# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: common.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='common.proto',
  package='shiftcrypto.bitbox02',
  syntax='proto3',
  serialized_pb=_b('\n\x0c\x63ommon.proto\x12\x14shiftcrypto.bitbox02\"\x1a\n\x0bPubResponse\x12\x0b\n\x03pub\x18\x01 \x01(\t\"\x18\n\x16RootFingerprintRequest\".\n\x17RootFingerprintResponse\x12\x13\n\x0b\x66ingerprint\x18\x01 \x01(\x0c\"l\n\x04XPub\x12\r\n\x05\x64\x65pth\x18\x01 \x01(\x0c\x12\x1a\n\x12parent_fingerprint\x18\x02 \x01(\x0c\x12\x11\n\tchild_num\x18\x03 \x01(\r\x12\x12\n\nchain_code\x18\x04 \x01(\x0c\x12\x12\n\npublic_key\x18\x05 \x01(\x0c\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_PUBRESPONSE = _descriptor.Descriptor(
  name='PubResponse',
  full_name='shiftcrypto.bitbox02.PubResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pub', full_name='shiftcrypto.bitbox02.PubResponse.pub', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=38,
  serialized_end=64,
)


_ROOTFINGERPRINTREQUEST = _descriptor.Descriptor(
  name='RootFingerprintRequest',
  full_name='shiftcrypto.bitbox02.RootFingerprintRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=66,
  serialized_end=90,
)


_ROOTFINGERPRINTRESPONSE = _descriptor.Descriptor(
  name='RootFingerprintResponse',
  full_name='shiftcrypto.bitbox02.RootFingerprintResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fingerprint', full_name='shiftcrypto.bitbox02.RootFingerprintResponse.fingerprint', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=92,
  serialized_end=138,
)


_XPUB = _descriptor.Descriptor(
  name='XPub',
  full_name='shiftcrypto.bitbox02.XPub',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='depth', full_name='shiftcrypto.bitbox02.XPub.depth', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='parent_fingerprint', full_name='shiftcrypto.bitbox02.XPub.parent_fingerprint', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='child_num', full_name='shiftcrypto.bitbox02.XPub.child_num', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='chain_code', full_name='shiftcrypto.bitbox02.XPub.chain_code', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='public_key', full_name='shiftcrypto.bitbox02.XPub.public_key', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=140,
  serialized_end=248,
)

DESCRIPTOR.message_types_by_name['PubResponse'] = _PUBRESPONSE
DESCRIPTOR.message_types_by_name['RootFingerprintRequest'] = _ROOTFINGERPRINTREQUEST
DESCRIPTOR.message_types_by_name['RootFingerprintResponse'] = _ROOTFINGERPRINTRESPONSE
DESCRIPTOR.message_types_by_name['XPub'] = _XPUB

PubResponse = _reflection.GeneratedProtocolMessageType('PubResponse', (_message.Message,), dict(
  DESCRIPTOR = _PUBRESPONSE,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:shiftcrypto.bitbox02.PubResponse)
  ))
_sym_db.RegisterMessage(PubResponse)

RootFingerprintRequest = _reflection.GeneratedProtocolMessageType('RootFingerprintRequest', (_message.Message,), dict(
  DESCRIPTOR = _ROOTFINGERPRINTREQUEST,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:shiftcrypto.bitbox02.RootFingerprintRequest)
  ))
_sym_db.RegisterMessage(RootFingerprintRequest)

RootFingerprintResponse = _reflection.GeneratedProtocolMessageType('RootFingerprintResponse', (_message.Message,), dict(
  DESCRIPTOR = _ROOTFINGERPRINTRESPONSE,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:shiftcrypto.bitbox02.RootFingerprintResponse)
  ))
_sym_db.RegisterMessage(RootFingerprintResponse)

XPub = _reflection.GeneratedProtocolMessageType('XPub', (_message.Message,), dict(
  DESCRIPTOR = _XPUB,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:shiftcrypto.bitbox02.XPub)
  ))
_sym_db.RegisterMessage(XPub)


# @@protoc_insertion_point(module_scope)
