# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from wandb.proto import wandb_internal_pb2 as wandb_dot_proto_dot_wandb__internal__pb2
from wandb.proto import wandb_server_pb2 as wandb_dot_proto_dot_wandb__server__pb2


class InternalServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.RunUpdate = channel.unary_unary(
        '/wandb_internal.InternalService/RunUpdate',
        request_serializer=wandb_dot_proto_dot_wandb__internal__pb2.RunData.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__server__pb2.RunUpdateResult.FromString,
        )
    self.RunExit = channel.unary_unary(
        '/wandb_internal.InternalService/RunExit',
        request_serializer=wandb_dot_proto_dot_wandb__internal__pb2.ExitData.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__server__pb2.RunExitResult.FromString,
        )
    self.Log = channel.unary_unary(
        '/wandb_internal.InternalService/Log',
        request_serializer=wandb_dot_proto_dot_wandb__internal__pb2.HistoryData.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__server__pb2.LogResult.FromString,
        )
    self.ServerShutdown = channel.unary_unary(
        '/wandb_internal.InternalService/ServerShutdown',
        request_serializer=wandb_dot_proto_dot_wandb__server__pb2.ServerShutdownRequest.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__server__pb2.ServerShutdownResult.FromString,
        )
    self.ServerStatus = channel.unary_unary(
        '/wandb_internal.InternalService/ServerStatus',
        request_serializer=wandb_dot_proto_dot_wandb__server__pb2.ServerStatusRequest.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__server__pb2.ServerStatusResult.FromString,
        )


class InternalServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def RunUpdate(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RunExit(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Log(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ServerShutdown(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ServerStatus(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_InternalServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'RunUpdate': grpc.unary_unary_rpc_method_handler(
          servicer.RunUpdate,
          request_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.RunData.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__server__pb2.RunUpdateResult.SerializeToString,
      ),
      'RunExit': grpc.unary_unary_rpc_method_handler(
          servicer.RunExit,
          request_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.ExitData.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__server__pb2.RunExitResult.SerializeToString,
      ),
      'Log': grpc.unary_unary_rpc_method_handler(
          servicer.Log,
          request_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.HistoryData.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__server__pb2.LogResult.SerializeToString,
      ),
      'ServerShutdown': grpc.unary_unary_rpc_method_handler(
          servicer.ServerShutdown,
          request_deserializer=wandb_dot_proto_dot_wandb__server__pb2.ServerShutdownRequest.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__server__pb2.ServerShutdownResult.SerializeToString,
      ),
      'ServerStatus': grpc.unary_unary_rpc_method_handler(
          servicer.ServerStatus,
          request_deserializer=wandb_dot_proto_dot_wandb__server__pb2.ServerStatusRequest.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__server__pb2.ServerStatusResult.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'wandb_internal.InternalService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
