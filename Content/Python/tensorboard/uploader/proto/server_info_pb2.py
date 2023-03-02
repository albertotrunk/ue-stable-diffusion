# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorboard/uploader/proto/server_info.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,tensorboard/uploader/proto/server_info.proto\x12\x13tensorboard.service\"l\n\x11ServerInfoRequest\x12\x0f\n\x07version\x18\x01 \x01(\t\x12\x46\n\x14plugin_specification\x18\x02 \x01(\x0b\x32(.tensorboard.service.PluginSpecification\"\xb7\x02\n\x12ServerInfoResponse\x12\x39\n\rcompatibility\x18\x01 \x01(\x0b\x32\".tensorboard.service.Compatibility\x12\x32\n\napi_server\x18\x02 \x01(\x0b\x32\x1e.tensorboard.service.ApiServer\x12<\n\nurl_format\x18\x03 \x01(\x0b\x32(.tensorboard.service.ExperimentUrlFormat\x12:\n\x0eplugin_control\x18\x04 \x01(\x0b\x32\".tensorboard.service.PluginControl\x12\x38\n\rupload_limits\x18\x05 \x01(\x0b\x32!.tensorboard.service.UploadLimits\"\\\n\rCompatibility\x12:\n\x07verdict\x18\x01 \x01(\x0e\x32).tensorboard.service.CompatibilityVerdict\x12\x0f\n\x07\x64\x65tails\x18\x02 \x01(\t\"\x1d\n\tApiServer\x12\x10\n\x08\x65ndpoint\x18\x01 \x01(\t\"?\n\x13\x45xperimentUrlFormat\x12\x10\n\x08template\x18\x01 \x01(\t\x12\x16\n\x0eid_placeholder\x18\x02 \x01(\t\"-\n\x13PluginSpecification\x12\x16\n\x0eupload_plugins\x18\x02 \x03(\t\"(\n\rPluginControl\x12\x17\n\x0f\x61llowed_plugins\x18\x01 \x03(\t\"\x92\x02\n\x0cUploadLimits\x12\x1f\n\x17max_scalar_request_size\x18\x03 \x01(\x03\x12\x1f\n\x17max_tensor_request_size\x18\x04 \x01(\x03\x12\x1d\n\x15max_blob_request_size\x18\x05 \x01(\x03\x12#\n\x1bmin_scalar_request_interval\x18\x06 \x01(\x03\x12#\n\x1bmin_tensor_request_interval\x18\x07 \x01(\x03\x12!\n\x19min_blob_request_interval\x18\x08 \x01(\x03\x12\x15\n\rmax_blob_size\x18\x01 \x01(\x03\x12\x1d\n\x15max_tensor_point_size\x18\x02 \x01(\x03*`\n\x14\x43ompatibilityVerdict\x12\x13\n\x0fVERDICT_UNKNOWN\x10\x00\x12\x0e\n\nVERDICT_OK\x10\x01\x12\x10\n\x0cVERDICT_WARN\x10\x02\x12\x11\n\rVERDICT_ERROR\x10\x03\x62\x06proto3')

_COMPATIBILITYVERDICT = DESCRIPTOR.enum_types_by_name['CompatibilityVerdict']
CompatibilityVerdict = enum_type_wrapper.EnumTypeWrapper(_COMPATIBILITYVERDICT)
VERDICT_UNKNOWN = 0
VERDICT_OK = 1
VERDICT_WARN = 2
VERDICT_ERROR = 3


_SERVERINFOREQUEST = DESCRIPTOR.message_types_by_name['ServerInfoRequest']
_SERVERINFORESPONSE = DESCRIPTOR.message_types_by_name['ServerInfoResponse']
_COMPATIBILITY = DESCRIPTOR.message_types_by_name['Compatibility']
_APISERVER = DESCRIPTOR.message_types_by_name['ApiServer']
_EXPERIMENTURLFORMAT = DESCRIPTOR.message_types_by_name['ExperimentUrlFormat']
_PLUGINSPECIFICATION = DESCRIPTOR.message_types_by_name['PluginSpecification']
_PLUGINCONTROL = DESCRIPTOR.message_types_by_name['PluginControl']
_UPLOADLIMITS = DESCRIPTOR.message_types_by_name['UploadLimits']
ServerInfoRequest = _reflection.GeneratedProtocolMessageType('ServerInfoRequest', (_message.Message,), {
  'DESCRIPTOR' : _SERVERINFOREQUEST,
  '__module__' : 'tensorboard.uploader.proto.server_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.ServerInfoRequest)
  })
_sym_db.RegisterMessage(ServerInfoRequest)

ServerInfoResponse = _reflection.GeneratedProtocolMessageType('ServerInfoResponse', (_message.Message,), {
  'DESCRIPTOR' : _SERVERINFORESPONSE,
  '__module__' : 'tensorboard.uploader.proto.server_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.ServerInfoResponse)
  })
_sym_db.RegisterMessage(ServerInfoResponse)

Compatibility = _reflection.GeneratedProtocolMessageType('Compatibility', (_message.Message,), {
  'DESCRIPTOR' : _COMPATIBILITY,
  '__module__' : 'tensorboard.uploader.proto.server_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.Compatibility)
  })
_sym_db.RegisterMessage(Compatibility)

ApiServer = _reflection.GeneratedProtocolMessageType('ApiServer', (_message.Message,), {
  'DESCRIPTOR' : _APISERVER,
  '__module__' : 'tensorboard.uploader.proto.server_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.ApiServer)
  })
_sym_db.RegisterMessage(ApiServer)

ExperimentUrlFormat = _reflection.GeneratedProtocolMessageType('ExperimentUrlFormat', (_message.Message,), {
  'DESCRIPTOR' : _EXPERIMENTURLFORMAT,
  '__module__' : 'tensorboard.uploader.proto.server_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.ExperimentUrlFormat)
  })
_sym_db.RegisterMessage(ExperimentUrlFormat)

PluginSpecification = _reflection.GeneratedProtocolMessageType('PluginSpecification', (_message.Message,), {
  'DESCRIPTOR' : _PLUGINSPECIFICATION,
  '__module__' : 'tensorboard.uploader.proto.server_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.PluginSpecification)
  })
_sym_db.RegisterMessage(PluginSpecification)

PluginControl = _reflection.GeneratedProtocolMessageType('PluginControl', (_message.Message,), {
  'DESCRIPTOR' : _PLUGINCONTROL,
  '__module__' : 'tensorboard.uploader.proto.server_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.PluginControl)
  })
_sym_db.RegisterMessage(PluginControl)

UploadLimits = _reflection.GeneratedProtocolMessageType('UploadLimits', (_message.Message,), {
  'DESCRIPTOR' : _UPLOADLIMITS,
  '__module__' : 'tensorboard.uploader.proto.server_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.UploadLimits)
  })
_sym_db.RegisterMessage(UploadLimits)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _COMPATIBILITYVERDICT._serialized_start=1049
  _COMPATIBILITYVERDICT._serialized_end=1145
  _SERVERINFOREQUEST._serialized_start=69
  _SERVERINFOREQUEST._serialized_end=177
  _SERVERINFORESPONSE._serialized_start=180
  _SERVERINFORESPONSE._serialized_end=491
  _COMPATIBILITY._serialized_start=493
  _COMPATIBILITY._serialized_end=585
  _APISERVER._serialized_start=587
  _APISERVER._serialized_end=616
  _EXPERIMENTURLFORMAT._serialized_start=618
  _EXPERIMENTURLFORMAT._serialized_end=681
  _PLUGINSPECIFICATION._serialized_start=683
  _PLUGINSPECIFICATION._serialized_end=728
  _PLUGINCONTROL._serialized_start=730
  _PLUGINCONTROL._serialized_end=770
  _UPLOADLIMITS._serialized_start=773
  _UPLOADLIMITS._serialized_end=1047
# @@protoc_insertion_point(module_scope)