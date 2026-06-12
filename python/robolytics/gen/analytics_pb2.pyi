from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AnalyticsQuery(_message.Message):
    __slots__ = ("metric", "group_by", "window", "filter")
    METRIC_FIELD_NUMBER: _ClassVar[int]
    GROUP_BY_FIELD_NUMBER: _ClassVar[int]
    WINDOW_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    metric: str
    group_by: str
    window: str
    filter: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, metric: _Optional[str] = ..., group_by: _Optional[str] = ..., window: _Optional[str] = ..., filter: _Optional[_Iterable[str]] = ...) -> None: ...

class MetricPoint(_message.Message):
    __slots__ = ("key", "value", "sample_count", "timestamp_ns")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_COUNT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_NS_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: float
    sample_count: int
    timestamp_ns: int
    def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ..., sample_count: _Optional[int] = ..., timestamp_ns: _Optional[int] = ...) -> None: ...

class AnalyticsResult(_message.Message):
    __slots__ = ("metric", "group_by", "points")
    METRIC_FIELD_NUMBER: _ClassVar[int]
    GROUP_BY_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    metric: str
    group_by: str
    points: _containers.RepeatedCompositeFieldContainer[MetricPoint]
    def __init__(self, metric: _Optional[str] = ..., group_by: _Optional[str] = ..., points: _Optional[_Iterable[_Union[MetricPoint, _Mapping]]] = ...) -> None: ...
