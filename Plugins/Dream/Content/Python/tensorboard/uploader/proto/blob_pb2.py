# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorboard/uploader/proto/blob.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%tensorboard/uploader/proto/blob.proto\x12\x13tensorboard.service\"F\n\x04\x42lob\x12\x0f\n\x07\x62lob_id\x18\x01 \x01(\t\x12-\n\x05state\x18\x02 \x01(\x0e\x32\x1e.tensorboard.service.BlobState\"<\n\x11\x42lobSequenceEntry\x12\'\n\x04\x62lob\x18\x01 \x01(\x0b\x32\x19.tensorboard.service.Blob\"G\n\x0c\x42lobSequence\x12\x37\n\x07\x65ntries\x18\x01 \x03(\x0b\x32&.tensorboard.service.BlobSequenceEntry*W\n\tBlobState\x12\x16\n\x12\x42LOB_STATE_UNKNOWN\x10\x00\x12\x1a\n\x16\x42LOB_STATE_UNFINALIZED\x10\x01\x12\x16\n\x12\x42LOB_STATE_CURRENT\x10\x02\x62\x06proto3')

_BLOBSTATE = DESCRIPTOR.enum_types_by_name['BlobState']
BlobState = enum_type_wrapper.EnumTypeWrapper(_BLOBSTATE)
BLOB_STATE_UNKNOWN = 0
BLOB_STATE_UNFINALIZED = 1
BLOB_STATE_CURRENT = 2


_BLOB = DESCRIPTOR.message_types_by_name['Blob']
_BLOBSEQUENCEENTRY = DESCRIPTOR.message_types_by_name['BlobSequenceEntry']
_BLOBSEQUENCE = DESCRIPTOR.message_types_by_name['BlobSequence']
Blob = _reflection.GeneratedProtocolMessageType('Blob', (_message.Message,), {
  'DESCRIPTOR' : _BLOB,
  '__module__' : 'tensorboard.uploader.proto.blob_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.Blob)
  })
_sym_db.RegisterMessage(Blob)

BlobSequenceEntry = _reflection.GeneratedProtocolMessageType('BlobSequenceEntry', (_message.Message,), {
  'DESCRIPTOR' : _BLOBSEQUENCEENTRY,
  '__module__' : 'tensorboard.uploader.proto.blob_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.BlobSequenceEntry)
  })
_sym_db.RegisterMessage(BlobSequenceEntry)

BlobSequence = _reflection.GeneratedProtocolMessageType('BlobSequence', (_message.Message,), {
  'DESCRIPTOR' : _BLOBSEQUENCE,
  '__module__' : 'tensorboard.uploader.proto.blob_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.BlobSequence)
  })
_sym_db.RegisterMessage(BlobSequence)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _BLOBSTATE._serialized_start=269
  _BLOBSTATE._serialized_end=356
  _BLOB._serialized_start=62
  _BLOB._serialized_end=132
  _BLOBSEQUENCEENTRY._serialized_start=134
  _BLOBSEQUENCEENTRY._serialized_end=194
  _BLOBSEQUENCE._serialized_start=196
  _BLOBSEQUENCE._serialized_end=267
# @@protoc_insertion_point(module_scope)
