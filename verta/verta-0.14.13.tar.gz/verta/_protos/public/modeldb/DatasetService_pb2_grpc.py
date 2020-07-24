# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from ..modeldb import CommonService_pb2 as modeldb_dot_CommonService__pb2
from ..modeldb import DatasetService_pb2 as modeldb_dot_DatasetService__pb2


class DatasetServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.createDataset = channel.unary_unary(
        '/ai.verta.modeldb.DatasetService/createDataset',
        request_serializer=modeldb_dot_DatasetService__pb2.CreateDataset.SerializeToString,
        response_deserializer=modeldb_dot_DatasetService__pb2.CreateDataset.Response.FromString,
        )
    self.getAllDatasets = channel.unary_unary(
        '/ai.verta.modeldb.DatasetService/getAllDatasets',
        request_serializer=modeldb_dot_DatasetService__pb2.GetAllDatasets.SerializeToString,
        response_deserializer=modeldb_dot_DatasetService__pb2.GetAllDatasets.Response.FromString,
        )
    self.getDatasetById = channel.unary_unary(
        '/ai.verta.modeldb.DatasetService/getDatasetById',
        request_serializer=modeldb_dot_DatasetService__pb2.GetDatasetById.SerializeToString,
        response_deserializer=modeldb_dot_DatasetService__pb2.GetDatasetById.Response.FromString,
        )
    self.getDatasetByName = channel.unary_unary(
        '/ai.verta.modeldb.DatasetService/getDatasetByName',
        request_serializer=modeldb_dot_DatasetService__pb2.GetDatasetByName.SerializeToString,
        response_deserializer=modeldb_dot_DatasetService__pb2.GetDatasetByName.Response.FromString,
        )
    self.deleteDataset = channel.unary_unary(
        '/ai.verta.modeldb.DatasetService/deleteDataset',
        request_serializer=modeldb_dot_DatasetService__pb2.DeleteDataset.SerializeToString,
        response_deserializer=modeldb_dot_DatasetService__pb2.DeleteDataset.Response.FromString,
        )
    self.deleteDatasets = channel.unary_unary(
        '/ai.verta.modeldb.DatasetService/deleteDatasets',
        request_serializer=modeldb_dot_DatasetService__pb2.DeleteDatasets.SerializeToString,
        response_deserializer=modeldb_dot_DatasetService__pb2.DeleteDatasets.Response.FromString,
        )
    self.findDatasets = channel.unary_unary(
        '/ai.verta.modeldb.DatasetService/findDatasets',
        request_serializer=modeldb_dot_DatasetService__pb2.FindDatasets.SerializeToString,
        response_deserializer=modeldb_dot_DatasetService__pb2.FindDatasets.Response.FromString,
        )
    self.updateDatasetName = channel.unary_unary(
        '/ai.verta.modeldb.DatasetService/updateDatasetName',
        request_serializer=modeldb_dot_DatasetService__pb2.UpdateDatasetName.SerializeToString,
        response_deserializer=modeldb_dot_DatasetService__pb2.UpdateDatasetName.Response.FromString,
        )
    self.updateDatasetDescription = channel.unary_unary(
        '/ai.verta.modeldb.DatasetService/updateDatasetDescription',
        request_serializer=modeldb_dot_DatasetService__pb2.UpdateDatasetDescription.SerializeToString,
        response_deserializer=modeldb_dot_DatasetService__pb2.UpdateDatasetDescription.Response.FromString,
        )
    self.addDatasetTags = channel.unary_unary(
        '/ai.verta.modeldb.DatasetService/addDatasetTags',
        request_serializer=modeldb_dot_DatasetService__pb2.AddDatasetTags.SerializeToString,
        response_deserializer=modeldb_dot_DatasetService__pb2.AddDatasetTags.Response.FromString,
        )
    self.getDatasetTags = channel.unary_unary(
        '/ai.verta.modeldb.DatasetService/getDatasetTags',
        request_serializer=modeldb_dot_CommonService__pb2.GetTags.SerializeToString,
        response_deserializer=modeldb_dot_CommonService__pb2.GetTags.Response.FromString,
        )
    self.deleteDatasetTags = channel.unary_unary(
        '/ai.verta.modeldb.DatasetService/deleteDatasetTags',
        request_serializer=modeldb_dot_DatasetService__pb2.DeleteDatasetTags.SerializeToString,
        response_deserializer=modeldb_dot_DatasetService__pb2.DeleteDatasetTags.Response.FromString,
        )
    self.addDatasetAttributes = channel.unary_unary(
        '/ai.verta.modeldb.DatasetService/addDatasetAttributes',
        request_serializer=modeldb_dot_DatasetService__pb2.AddDatasetAttributes.SerializeToString,
        response_deserializer=modeldb_dot_DatasetService__pb2.AddDatasetAttributes.Response.FromString,
        )
    self.updateDatasetAttributes = channel.unary_unary(
        '/ai.verta.modeldb.DatasetService/updateDatasetAttributes',
        request_serializer=modeldb_dot_DatasetService__pb2.UpdateDatasetAttributes.SerializeToString,
        response_deserializer=modeldb_dot_DatasetService__pb2.UpdateDatasetAttributes.Response.FromString,
        )
    self.deleteDatasetAttributes = channel.unary_unary(
        '/ai.verta.modeldb.DatasetService/deleteDatasetAttributes',
        request_serializer=modeldb_dot_DatasetService__pb2.DeleteDatasetAttributes.SerializeToString,
        response_deserializer=modeldb_dot_DatasetService__pb2.DeleteDatasetAttributes.Response.FromString,
        )
    self.setDatasetVisibility = channel.unary_unary(
        '/ai.verta.modeldb.DatasetService/setDatasetVisibility',
        request_serializer=modeldb_dot_DatasetService__pb2.SetDatasetVisibilty.SerializeToString,
        response_deserializer=modeldb_dot_DatasetService__pb2.SetDatasetVisibilty.Response.FromString,
        )
    self.getLastExperimentByDatasetId = channel.unary_unary(
        '/ai.verta.modeldb.DatasetService/getLastExperimentByDatasetId',
        request_serializer=modeldb_dot_DatasetService__pb2.LastExperimentByDatasetId.SerializeToString,
        response_deserializer=modeldb_dot_DatasetService__pb2.LastExperimentByDatasetId.Response.FromString,
        )
    self.getExperimentRunByDataset = channel.unary_unary(
        '/ai.verta.modeldb.DatasetService/getExperimentRunByDataset',
        request_serializer=modeldb_dot_DatasetService__pb2.GetExperimentRunByDataset.SerializeToString,
        response_deserializer=modeldb_dot_DatasetService__pb2.GetExperimentRunByDataset.Response.FromString,
        )
    self.setDatasetWorkspace = channel.unary_unary(
        '/ai.verta.modeldb.DatasetService/setDatasetWorkspace',
        request_serializer=modeldb_dot_DatasetService__pb2.SetDatasetWorkspace.SerializeToString,
        response_deserializer=modeldb_dot_DatasetService__pb2.SetDatasetWorkspace.Response.FromString,
        )


class DatasetServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def createDataset(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getAllDatasets(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getDatasetById(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getDatasetByName(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def deleteDataset(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def deleteDatasets(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def findDatasets(self, request, context):
    """queries
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def updateDatasetName(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def updateDatasetDescription(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def addDatasetTags(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getDatasetTags(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def deleteDatasetTags(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def addDatasetAttributes(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def updateDatasetAttributes(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def deleteDatasetAttributes(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def setDatasetVisibility(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getLastExperimentByDatasetId(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getExperimentRunByDataset(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def setDatasetWorkspace(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_DatasetServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'createDataset': grpc.unary_unary_rpc_method_handler(
          servicer.createDataset,
          request_deserializer=modeldb_dot_DatasetService__pb2.CreateDataset.FromString,
          response_serializer=modeldb_dot_DatasetService__pb2.CreateDataset.Response.SerializeToString,
      ),
      'getAllDatasets': grpc.unary_unary_rpc_method_handler(
          servicer.getAllDatasets,
          request_deserializer=modeldb_dot_DatasetService__pb2.GetAllDatasets.FromString,
          response_serializer=modeldb_dot_DatasetService__pb2.GetAllDatasets.Response.SerializeToString,
      ),
      'getDatasetById': grpc.unary_unary_rpc_method_handler(
          servicer.getDatasetById,
          request_deserializer=modeldb_dot_DatasetService__pb2.GetDatasetById.FromString,
          response_serializer=modeldb_dot_DatasetService__pb2.GetDatasetById.Response.SerializeToString,
      ),
      'getDatasetByName': grpc.unary_unary_rpc_method_handler(
          servicer.getDatasetByName,
          request_deserializer=modeldb_dot_DatasetService__pb2.GetDatasetByName.FromString,
          response_serializer=modeldb_dot_DatasetService__pb2.GetDatasetByName.Response.SerializeToString,
      ),
      'deleteDataset': grpc.unary_unary_rpc_method_handler(
          servicer.deleteDataset,
          request_deserializer=modeldb_dot_DatasetService__pb2.DeleteDataset.FromString,
          response_serializer=modeldb_dot_DatasetService__pb2.DeleteDataset.Response.SerializeToString,
      ),
      'deleteDatasets': grpc.unary_unary_rpc_method_handler(
          servicer.deleteDatasets,
          request_deserializer=modeldb_dot_DatasetService__pb2.DeleteDatasets.FromString,
          response_serializer=modeldb_dot_DatasetService__pb2.DeleteDatasets.Response.SerializeToString,
      ),
      'findDatasets': grpc.unary_unary_rpc_method_handler(
          servicer.findDatasets,
          request_deserializer=modeldb_dot_DatasetService__pb2.FindDatasets.FromString,
          response_serializer=modeldb_dot_DatasetService__pb2.FindDatasets.Response.SerializeToString,
      ),
      'updateDatasetName': grpc.unary_unary_rpc_method_handler(
          servicer.updateDatasetName,
          request_deserializer=modeldb_dot_DatasetService__pb2.UpdateDatasetName.FromString,
          response_serializer=modeldb_dot_DatasetService__pb2.UpdateDatasetName.Response.SerializeToString,
      ),
      'updateDatasetDescription': grpc.unary_unary_rpc_method_handler(
          servicer.updateDatasetDescription,
          request_deserializer=modeldb_dot_DatasetService__pb2.UpdateDatasetDescription.FromString,
          response_serializer=modeldb_dot_DatasetService__pb2.UpdateDatasetDescription.Response.SerializeToString,
      ),
      'addDatasetTags': grpc.unary_unary_rpc_method_handler(
          servicer.addDatasetTags,
          request_deserializer=modeldb_dot_DatasetService__pb2.AddDatasetTags.FromString,
          response_serializer=modeldb_dot_DatasetService__pb2.AddDatasetTags.Response.SerializeToString,
      ),
      'getDatasetTags': grpc.unary_unary_rpc_method_handler(
          servicer.getDatasetTags,
          request_deserializer=modeldb_dot_CommonService__pb2.GetTags.FromString,
          response_serializer=modeldb_dot_CommonService__pb2.GetTags.Response.SerializeToString,
      ),
      'deleteDatasetTags': grpc.unary_unary_rpc_method_handler(
          servicer.deleteDatasetTags,
          request_deserializer=modeldb_dot_DatasetService__pb2.DeleteDatasetTags.FromString,
          response_serializer=modeldb_dot_DatasetService__pb2.DeleteDatasetTags.Response.SerializeToString,
      ),
      'addDatasetAttributes': grpc.unary_unary_rpc_method_handler(
          servicer.addDatasetAttributes,
          request_deserializer=modeldb_dot_DatasetService__pb2.AddDatasetAttributes.FromString,
          response_serializer=modeldb_dot_DatasetService__pb2.AddDatasetAttributes.Response.SerializeToString,
      ),
      'updateDatasetAttributes': grpc.unary_unary_rpc_method_handler(
          servicer.updateDatasetAttributes,
          request_deserializer=modeldb_dot_DatasetService__pb2.UpdateDatasetAttributes.FromString,
          response_serializer=modeldb_dot_DatasetService__pb2.UpdateDatasetAttributes.Response.SerializeToString,
      ),
      'deleteDatasetAttributes': grpc.unary_unary_rpc_method_handler(
          servicer.deleteDatasetAttributes,
          request_deserializer=modeldb_dot_DatasetService__pb2.DeleteDatasetAttributes.FromString,
          response_serializer=modeldb_dot_DatasetService__pb2.DeleteDatasetAttributes.Response.SerializeToString,
      ),
      'setDatasetVisibility': grpc.unary_unary_rpc_method_handler(
          servicer.setDatasetVisibility,
          request_deserializer=modeldb_dot_DatasetService__pb2.SetDatasetVisibilty.FromString,
          response_serializer=modeldb_dot_DatasetService__pb2.SetDatasetVisibilty.Response.SerializeToString,
      ),
      'getLastExperimentByDatasetId': grpc.unary_unary_rpc_method_handler(
          servicer.getLastExperimentByDatasetId,
          request_deserializer=modeldb_dot_DatasetService__pb2.LastExperimentByDatasetId.FromString,
          response_serializer=modeldb_dot_DatasetService__pb2.LastExperimentByDatasetId.Response.SerializeToString,
      ),
      'getExperimentRunByDataset': grpc.unary_unary_rpc_method_handler(
          servicer.getExperimentRunByDataset,
          request_deserializer=modeldb_dot_DatasetService__pb2.GetExperimentRunByDataset.FromString,
          response_serializer=modeldb_dot_DatasetService__pb2.GetExperimentRunByDataset.Response.SerializeToString,
      ),
      'setDatasetWorkspace': grpc.unary_unary_rpc_method_handler(
          servicer.setDatasetWorkspace,
          request_deserializer=modeldb_dot_DatasetService__pb2.SetDatasetWorkspace.FromString,
          response_serializer=modeldb_dot_DatasetService__pb2.SetDatasetWorkspace.Response.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ai.verta.modeldb.DatasetService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
