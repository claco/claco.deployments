from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
DR_FAILURE: DeploymentResult
DR_SUCCESS: DeploymentResult
DR_UNSPECIFIED: DeploymentResult
DSRC_ERROR: DeploymentServiceResultCode
DSRC_OK: DeploymentServiceResultCode
DSRC_UNSPECIFIED: DeploymentServiceResultCode
DS_COMPLETED: DeploymentStatus
DS_CREATED: DeploymentStatus
DS_DELETED: DeploymentStatus
DS_QUEUED: DeploymentStatus
DS_STARTED: DeploymentStatus
DS_UNSPECIFIED: DeploymentStatus

class CreateDeploymentRequest(_message.Message):
    __slots__ = ["image"]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    image: str
    def __init__(self, image: _Optional[str] = ...) -> None: ...

class CreateDeploymentResponse(_message.Message):
    __slots__ = ["deployment", "result"]
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    deployment: Deployment
    result: DeploymentServiceRequestResult
    def __init__(self, result: _Optional[_Union[DeploymentServiceRequestResult, _Mapping]] = ..., deployment: _Optional[_Union[Deployment, _Mapping]] = ...) -> None: ...

class DeleteDeploymentRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteDeploymentResponse(_message.Message):
    __slots__ = ["deployment", "result"]
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    deployment: Deployment
    result: DeploymentServiceRequestResult
    def __init__(self, result: _Optional[_Union[DeploymentServiceRequestResult, _Mapping]] = ..., deployment: _Optional[_Union[Deployment, _Mapping]] = ...) -> None: ...

class Deployment(_message.Message):
    __slots__ = ["id", "image", "result", "status"]
    ID_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    image: str
    result: DeploymentResult
    status: DeploymentStatus
    def __init__(self, id: _Optional[str] = ..., image: _Optional[str] = ..., status: _Optional[_Union[DeploymentStatus, str]] = ..., result: _Optional[_Union[DeploymentResult, str]] = ...) -> None: ...

class DeploymentServiceEvent(_message.Message):
    __slots__ = ["detail", "event"]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    detail: _struct_pb2.Struct
    event: str
    def __init__(self, event: _Optional[str] = ..., detail: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class DeploymentServiceRequestResult(_message.Message):
    __slots__ = ["code", "events", "message"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: DeploymentServiceResultCode
    events: _containers.RepeatedCompositeFieldContainer[DeploymentServiceEvent]
    message: str
    def __init__(self, code: _Optional[_Union[DeploymentServiceResultCode, str]] = ..., message: _Optional[str] = ..., events: _Optional[_Iterable[_Union[DeploymentServiceEvent, _Mapping]]] = ...) -> None: ...

class QueueDeploymentRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class QueueDeploymentResponse(_message.Message):
    __slots__ = ["deployment", "result"]
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    deployment: Deployment
    result: DeploymentServiceRequestResult
    def __init__(self, result: _Optional[_Union[DeploymentServiceRequestResult, _Mapping]] = ..., deployment: _Optional[_Union[Deployment, _Mapping]] = ...) -> None: ...

class DeploymentServiceResultCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class DeploymentStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class DeploymentResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
