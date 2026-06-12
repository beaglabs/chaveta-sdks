from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MissionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MISSION_STATUS_UNSPECIFIED: _ClassVar[MissionStatus]
    MISSION_STATUS_SUCCESS: _ClassVar[MissionStatus]
    MISSION_STATUS_FAILURE: _ClassVar[MissionStatus]
    MISSION_STATUS_TIMEOUT: _ClassVar[MissionStatus]
    MISSION_STATUS_INTERVENTION: _ClassVar[MissionStatus]
MISSION_STATUS_UNSPECIFIED: MissionStatus
MISSION_STATUS_SUCCESS: MissionStatus
MISSION_STATUS_FAILURE: MissionStatus
MISSION_STATUS_TIMEOUT: MissionStatus
MISSION_STATUS_INTERVENTION: MissionStatus

class Pose3D(_message.Message):
    __slots__ = ("x", "y", "z", "roll", "pitch", "yaw")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    ROLL_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    z: float
    roll: float
    pitch: float
    yaw: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ..., roll: _Optional[float] = ..., pitch: _Optional[float] = ..., yaw: _Optional[float] = ...) -> None: ...

class MetricDelta(_message.Message):
    __slots__ = ("metric_name", "baseline_value", "current_value", "delta_pct")
    METRIC_NAME_FIELD_NUMBER: _ClassVar[int]
    BASELINE_VALUE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_VALUE_FIELD_NUMBER: _ClassVar[int]
    DELTA_PCT_FIELD_NUMBER: _ClassVar[int]
    metric_name: str
    baseline_value: float
    current_value: float
    delta_pct: float
    def __init__(self, metric_name: _Optional[str] = ..., baseline_value: _Optional[float] = ..., current_value: _Optional[float] = ..., delta_pct: _Optional[float] = ...) -> None: ...
