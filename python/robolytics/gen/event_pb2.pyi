import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScenarioStarted(_message.Message):
    __slots__ = ("scenario_id", "scenario_name", "domain", "params", "seed", "software_version", "repo")
    class ParamsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SCENARIO_ID_FIELD_NUMBER: _ClassVar[int]
    SCENARIO_NAME_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    SOFTWARE_VERSION_FIELD_NUMBER: _ClassVar[int]
    REPO_FIELD_NUMBER: _ClassVar[int]
    scenario_id: str
    scenario_name: str
    domain: str
    params: _containers.ScalarMap[str, str]
    seed: str
    software_version: str
    repo: str
    def __init__(self, scenario_id: _Optional[str] = ..., scenario_name: _Optional[str] = ..., domain: _Optional[str] = ..., params: _Optional[_Mapping[str, str]] = ..., seed: _Optional[str] = ..., software_version: _Optional[str] = ..., repo: _Optional[str] = ...) -> None: ...

class MissionCompleted(_message.Message):
    __slots__ = ("scenario_id", "mission_id", "status", "metrics", "software_version")
    class MetricsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    SCENARIO_ID_FIELD_NUMBER: _ClassVar[int]
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    SOFTWARE_VERSION_FIELD_NUMBER: _ClassVar[int]
    scenario_id: str
    mission_id: str
    status: _types_pb2.MissionStatus
    metrics: _containers.ScalarMap[str, float]
    software_version: str
    def __init__(self, scenario_id: _Optional[str] = ..., mission_id: _Optional[str] = ..., status: _Optional[_Union[_types_pb2.MissionStatus, str]] = ..., metrics: _Optional[_Mapping[str, float]] = ..., software_version: _Optional[str] = ...) -> None: ...

class PerceptionMetric(_message.Message):
    __slots__ = ("scenario_id", "class_name", "confidence", "iou", "true_positive", "false_positive", "false_negative", "position")
    SCENARIO_ID_FIELD_NUMBER: _ClassVar[int]
    CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    IOU_FIELD_NUMBER: _ClassVar[int]
    TRUE_POSITIVE_FIELD_NUMBER: _ClassVar[int]
    FALSE_POSITIVE_FIELD_NUMBER: _ClassVar[int]
    FALSE_NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    scenario_id: str
    class_name: str
    confidence: float
    iou: float
    true_positive: bool
    false_positive: bool
    false_negative: bool
    position: _types_pb2.Pose3D
    def __init__(self, scenario_id: _Optional[str] = ..., class_name: _Optional[str] = ..., confidence: _Optional[float] = ..., iou: _Optional[float] = ..., true_positive: _Optional[bool] = ..., false_positive: _Optional[bool] = ..., false_negative: _Optional[bool] = ..., position: _Optional[_Union[_types_pb2.Pose3D, _Mapping]] = ...) -> None: ...

class PolicyDecision(_message.Message):
    __slots__ = ("scenario_id", "mission_id", "step", "action", "state", "reward")
    SCENARIO_ID_FIELD_NUMBER: _ClassVar[int]
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    REWARD_FIELD_NUMBER: _ClassVar[int]
    scenario_id: str
    mission_id: str
    step: int
    action: _containers.RepeatedScalarFieldContainer[float]
    state: _containers.RepeatedScalarFieldContainer[float]
    reward: float
    def __init__(self, scenario_id: _Optional[str] = ..., mission_id: _Optional[str] = ..., step: _Optional[int] = ..., action: _Optional[_Iterable[float]] = ..., state: _Optional[_Iterable[float]] = ..., reward: _Optional[float] = ...) -> None: ...

class RegressionDetected(_message.Message):
    __slots__ = ("scenario_id", "baseline_id", "evaluation_id", "deltas", "severity")
    SCENARIO_ID_FIELD_NUMBER: _ClassVar[int]
    BASELINE_ID_FIELD_NUMBER: _ClassVar[int]
    EVALUATION_ID_FIELD_NUMBER: _ClassVar[int]
    DELTAS_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    scenario_id: str
    baseline_id: str
    evaluation_id: str
    deltas: _containers.RepeatedCompositeFieldContainer[_types_pb2.MetricDelta]
    severity: str
    def __init__(self, scenario_id: _Optional[str] = ..., baseline_id: _Optional[str] = ..., evaluation_id: _Optional[str] = ..., deltas: _Optional[_Iterable[_Union[_types_pb2.MetricDelta, _Mapping]]] = ..., severity: _Optional[str] = ...) -> None: ...

class SensorTelemetry(_message.Message):
    __slots__ = ("sensor_id", "sensor_type", "utilization_pct", "frame_count", "data_rate_mbps", "error_count")
    SENSOR_ID_FIELD_NUMBER: _ClassVar[int]
    SENSOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    UTILIZATION_PCT_FIELD_NUMBER: _ClassVar[int]
    FRAME_COUNT_FIELD_NUMBER: _ClassVar[int]
    DATA_RATE_MBPS_FIELD_NUMBER: _ClassVar[int]
    ERROR_COUNT_FIELD_NUMBER: _ClassVar[int]
    sensor_id: str
    sensor_type: str
    utilization_pct: float
    frame_count: int
    data_rate_mbps: float
    error_count: int
    def __init__(self, sensor_id: _Optional[str] = ..., sensor_type: _Optional[str] = ..., utilization_pct: _Optional[float] = ..., frame_count: _Optional[int] = ..., data_rate_mbps: _Optional[float] = ..., error_count: _Optional[int] = ...) -> None: ...

class Sim2RealGap(_message.Message):
    __slots__ = ("scenario_id", "sim_metrics", "real_metrics", "gap_pct")
    class SimMetricsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    class RealMetricsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    class GapPctEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    SCENARIO_ID_FIELD_NUMBER: _ClassVar[int]
    SIM_METRICS_FIELD_NUMBER: _ClassVar[int]
    REAL_METRICS_FIELD_NUMBER: _ClassVar[int]
    GAP_PCT_FIELD_NUMBER: _ClassVar[int]
    scenario_id: str
    sim_metrics: _containers.ScalarMap[str, float]
    real_metrics: _containers.ScalarMap[str, float]
    gap_pct: _containers.ScalarMap[str, float]
    def __init__(self, scenario_id: _Optional[str] = ..., sim_metrics: _Optional[_Mapping[str, float]] = ..., real_metrics: _Optional[_Mapping[str, float]] = ..., gap_pct: _Optional[_Mapping[str, float]] = ...) -> None: ...

class ActionTaken(_message.Message):
    __slots__ = ("scenario_id", "mission_id", "step", "action", "state", "position")
    SCENARIO_ID_FIELD_NUMBER: _ClassVar[int]
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    scenario_id: str
    mission_id: str
    step: int
    action: _containers.RepeatedScalarFieldContainer[float]
    state: _containers.RepeatedScalarFieldContainer[float]
    position: _types_pb2.Pose3D
    def __init__(self, scenario_id: _Optional[str] = ..., mission_id: _Optional[str] = ..., step: _Optional[int] = ..., action: _Optional[_Iterable[float]] = ..., state: _Optional[_Iterable[float]] = ..., position: _Optional[_Union[_types_pb2.Pose3D, _Mapping]] = ...) -> None: ...

class ObstacleEncountered(_message.Message):
    __slots__ = ("scenario_id", "mission_id", "step", "obstacle_class", "position", "relative_speed", "collision", "video_r2_key")
    SCENARIO_ID_FIELD_NUMBER: _ClassVar[int]
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    OBSTACLE_CLASS_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_SPEED_FIELD_NUMBER: _ClassVar[int]
    COLLISION_FIELD_NUMBER: _ClassVar[int]
    VIDEO_R2_KEY_FIELD_NUMBER: _ClassVar[int]
    scenario_id: str
    mission_id: str
    step: int
    obstacle_class: str
    position: _types_pb2.Pose3D
    relative_speed: float
    collision: bool
    video_r2_key: str
    def __init__(self, scenario_id: _Optional[str] = ..., mission_id: _Optional[str] = ..., step: _Optional[int] = ..., obstacle_class: _Optional[str] = ..., position: _Optional[_Union[_types_pb2.Pose3D, _Mapping]] = ..., relative_speed: _Optional[float] = ..., collision: _Optional[bool] = ..., video_r2_key: _Optional[str] = ...) -> None: ...

class ObjectIdentified(_message.Message):
    __slots__ = ("scenario_id", "mission_id", "class_name", "confidence", "position", "sensor_origin")
    SCENARIO_ID_FIELD_NUMBER: _ClassVar[int]
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    SENSOR_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    scenario_id: str
    mission_id: str
    class_name: str
    confidence: float
    position: _types_pb2.Pose3D
    sensor_origin: _types_pb2.Pose3D
    def __init__(self, scenario_id: _Optional[str] = ..., mission_id: _Optional[str] = ..., class_name: _Optional[str] = ..., confidence: _Optional[float] = ..., position: _Optional[_Union[_types_pb2.Pose3D, _Mapping]] = ..., sensor_origin: _Optional[_Union[_types_pb2.Pose3D, _Mapping]] = ...) -> None: ...

class RobolyticsEvent(_message.Message):
    __slots__ = ("event_id", "timestamp_ns", "source", "source_version", "scenario_started", "mission_completed", "perception_metric", "policy_decision", "regression_detected", "sensor_telemetry", "sim2real_gap", "action_taken", "obstacle_encountered", "object_identified")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_NS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_VERSION_FIELD_NUMBER: _ClassVar[int]
    SCENARIO_STARTED_FIELD_NUMBER: _ClassVar[int]
    MISSION_COMPLETED_FIELD_NUMBER: _ClassVar[int]
    PERCEPTION_METRIC_FIELD_NUMBER: _ClassVar[int]
    POLICY_DECISION_FIELD_NUMBER: _ClassVar[int]
    REGRESSION_DETECTED_FIELD_NUMBER: _ClassVar[int]
    SENSOR_TELEMETRY_FIELD_NUMBER: _ClassVar[int]
    SIM2REAL_GAP_FIELD_NUMBER: _ClassVar[int]
    ACTION_TAKEN_FIELD_NUMBER: _ClassVar[int]
    OBSTACLE_ENCOUNTERED_FIELD_NUMBER: _ClassVar[int]
    OBJECT_IDENTIFIED_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    timestamp_ns: int
    source: str
    source_version: str
    scenario_started: ScenarioStarted
    mission_completed: MissionCompleted
    perception_metric: PerceptionMetric
    policy_decision: PolicyDecision
    regression_detected: RegressionDetected
    sensor_telemetry: SensorTelemetry
    sim2real_gap: Sim2RealGap
    action_taken: ActionTaken
    obstacle_encountered: ObstacleEncountered
    object_identified: ObjectIdentified
    def __init__(self, event_id: _Optional[str] = ..., timestamp_ns: _Optional[int] = ..., source: _Optional[str] = ..., source_version: _Optional[str] = ..., scenario_started: _Optional[_Union[ScenarioStarted, _Mapping]] = ..., mission_completed: _Optional[_Union[MissionCompleted, _Mapping]] = ..., perception_metric: _Optional[_Union[PerceptionMetric, _Mapping]] = ..., policy_decision: _Optional[_Union[PolicyDecision, _Mapping]] = ..., regression_detected: _Optional[_Union[RegressionDetected, _Mapping]] = ..., sensor_telemetry: _Optional[_Union[SensorTelemetry, _Mapping]] = ..., sim2real_gap: _Optional[_Union[Sim2RealGap, _Mapping]] = ..., action_taken: _Optional[_Union[ActionTaken, _Mapping]] = ..., obstacle_encountered: _Optional[_Union[ObstacleEncountered, _Mapping]] = ..., object_identified: _Optional[_Union[ObjectIdentified, _Mapping]] = ...) -> None: ...
