import enum
from typing import List, Optional

import redvox.api1000.common.typing
import redvox.api1000.proto.redvox_api_m_pb2 as redvox_api_m_pb2
import redvox.api1000.common.common as common
import redvox.api1000.common.generic

_NETWORK_TYPE_FIELD_NAME: str = "network_type"
_CELL_SERVICE_STATE_FIELD_NAME: str = "cell_service_state"
_POWER_STATE_FIELD_NAME: str = "power_state"
_ADDITIONAL_INPUT_SENSORS_FIELD_NAME: str = "additional_input_sensors"

InputSensorProto = redvox_api_m_pb2.RedvoxPacketM.StationInformation.AppSettings.InputSensor


class AudioSamplingRate(enum.Enum):
    UNKNOWN_SAMPLING_RATE: int = 0
    HZ_80: int = 1
    HZ_800: int = 2
    HZ_8000: int = 3
    HZ_16000: int = 4
    HZ_48000: int = 5

    @staticmethod
    def from_proto(
            audio_sample_rate: redvox_api_m_pb2.RedvoxPacketM.StationInformation.AppSettings.AudioSamplingRate) -> 'AudioSamplingRate':
        return AudioSamplingRate(audio_sample_rate)

    def into_proto(self) -> redvox_api_m_pb2.RedvoxPacketM.StationInformation.AppSettings.AudioSamplingRate:
        return redvox_api_m_pb2.RedvoxPacketM.StationInformation.AppSettings.AudioSamplingRate.Value(self.name)

    @staticmethod
    def from_sampling_rate(sampling_rate: float) -> Optional['AudioSamplingRate']:
        if sampling_rate == 80.0:
            return AudioSamplingRate['HZ_80']
        elif sampling_rate == 800.0:
            return AudioSamplingRate['HZ_800']
        elif sampling_rate == 8000.0:
            return AudioSamplingRate['HZ_8000']
        elif sampling_rate == 16000.0:
            return AudioSamplingRate['HZ_16000']
        elif sampling_rate == 48000.0:
            return AudioSamplingRate['HZ_48000']
        else:
            return AudioSamplingRate['UNKNOWN_SAMPLING_RATE']


class AudioSourceTuning(enum.Enum):
    UNKNOWN_TUNING: int = 0
    INFRASOUND_TUNING: int = 1
    LOW_AUDIO_TUNING: int = 2
    AUDIO_TUNING: int = 3

    @staticmethod
    def from_proto(
            audio_source_tuning: redvox_api_m_pb2.RedvoxPacketM.StationInformation.AppSettings.AudioSourceTuning) -> 'AudioSourceTuning':
        return AudioSourceTuning(audio_source_tuning)

    def into_proto(self) -> redvox_api_m_pb2.RedvoxPacketM.StationInformation.AppSettings.AudioSourceTuning:
        return redvox_api_m_pb2.RedvoxPacketM.StationInformation.AppSettings.AudioSourceTuning.Value(self.name)


class InputSensor(enum.Enum):
    UNKNOWN_SENSOR: int = 0
    ACCELEROMETER = 1
    AMBIENT_TEMPERATURE = 2
    AUDIO = 3
    COMPRESSED_AUDIO = 4
    GRAVITY = 5
    GYROSCOPE = 6
    IMAGE = 7
    LIGHT = 8
    LINEAR_ACCELERATION = 9
    LOCATION = 10
    MAGNETOMETER = 11
    ORIENTATION = 12
    PRESSURE = 13
    PROXIMITY = 14
    RELATIVE_HUMIDITY = 15
    ROTATION_VECTOR = 16

    @staticmethod
    def from_proto(
            input_sensor: redvox_api_m_pb2.RedvoxPacketM.StationInformation.AppSettings.InputSensor) -> 'InputSensor':
        return InputSensor(input_sensor)

    def into_proto(self) -> redvox_api_m_pb2.RedvoxPacketM.StationInformation.AppSettings.InputSensor:
        return redvox_api_m_pb2.RedvoxPacketM.StationInformation.AppSettings.InputSensor.Value(self.name)


class FftOverlap(enum.Enum):
    UNKNOWN: int = 0
    PERCENT_25: int = 1
    PERCENT_50: int = 2
    PERCENT_75: int = 3

    @staticmethod
    def from_proto(
            fft_overlap: redvox_api_m_pb2.RedvoxPacketM.StationInformation.AppSettings.FftOverlap) -> 'FftOverlap':
        return FftOverlap(fft_overlap)

    def into_proto(self) -> redvox_api_m_pb2.RedvoxPacketM.StationInformation.AppSettings.FftOverlap:
        return redvox_api_m_pb2.RedvoxPacketM.StationInformation.AppSettings.FftOverlap.Value(self.name)


class AppSettings(
    redvox.api1000.common.generic.ProtoBase[redvox_api_m_pb2.RedvoxPacketM.StationInformation.AppSettings]):
    def __init__(self, proto: redvox_api_m_pb2.RedvoxPacketM.StationInformation.AppSettings):
        super().__init__(proto)
        self._additional_input_sensors: redvox.api1000.common.generic.ProtoRepeatedMessage[InputSensorProto, InputSensor] =\
            redvox.api1000.common.generic.ProtoRepeatedMessage(
            proto,
            proto.additional_input_sensors,
            _ADDITIONAL_INPUT_SENSORS_FIELD_NAME,
            InputSensor.from_proto,
            InputSensor.into_proto
        )

    @staticmethod
    def new() -> 'AppSettings':
        return AppSettings(redvox_api_m_pb2.RedvoxPacketM.StationInformation.AppSettings())

    def get_audio_sampling_rate(self) -> AudioSamplingRate:
        return AudioSamplingRate(self.get_proto().audio_sampling_rate)

    def set_audio_sampling_rate(self, audio_sampling_rate: AudioSamplingRate) -> 'AppSettings':
        redvox.api1000.common.typing.check_type(audio_sampling_rate, [AudioSamplingRate])

        self.get_proto().audio_sampling_rate = redvox_api_m_pb2.RedvoxPacketM.StationInformation.AppSettings.AudioSamplingRate.Value(
            audio_sampling_rate.name)
        return self

    def get_audio_source_tuning(self) -> AudioSourceTuning:
        return AudioSourceTuning(self.get_proto().audio_source_tuning)

    def set_audio_source_tuning(self, audio_source_tuning: AudioSourceTuning) -> 'AppSettings':
        redvox.api1000.common.typing.check_type(audio_source_tuning, [AudioSourceTuning])

        self.get_proto().audio_source_tuning = redvox_api_m_pb2.RedvoxPacketM.StationInformation.AppSettings.AudioSourceTuning.Value(
            audio_source_tuning.name)
        return self

    def get_additional_input_sensors(self) -> redvox.api1000.common.generic.ProtoRepeatedMessage:
        return self._additional_input_sensors

    def get_fft_overlap(self) -> FftOverlap:
        return FftOverlap(self.get_proto().fft_overlap)

    def set_fft_overlap(self, fft_overlap: FftOverlap) -> 'AppSettings':
        redvox.api1000.common.typing.check_type(fft_overlap, [FftOverlap])

        self.get_proto().fft_overlap = redvox_api_m_pb2.RedvoxPacketM.StationInformation.AppSettings.FftOverlap.Value(
            fft_overlap.name)
        return self

    def get_automatically_record(self) -> bool:
        return self.get_proto().automatically_record

    def set_automatically_record(self, automatically_record: bool) -> 'AppSettings':
        redvox.api1000.common.typing.check_type(automatically_record, [bool])
        self.get_proto().automatically_record = automatically_record
        return self

    def get_launch_at_power_up(self) -> bool:
        return self.get_proto().launch_at_power_up

    def set_launch_at_power_up(self, launch_at_power_up: bool) -> 'AppSettings':
        redvox.api1000.common.typing.check_type(launch_at_power_up, [bool])
        self.get_proto().launch_at_power_up = launch_at_power_up
        return self

    def get_station_id(self) -> str:
        return self.get_proto().station_id

    def set_station_id(self, station_id: str) -> 'AppSettings':
        redvox.api1000.common.typing.check_type(station_id, [str])
        self.get_proto().station_id = station_id
        return self

    def get_push_to_server(self) -> bool:
        return self.get_proto().push_to_server

    def set_push_to_server(self, push_to_server: bool) -> 'AppSettings':
        redvox.api1000.common.typing.check_type(push_to_server, [bool])
        self.get_proto().push_to_server = push_to_server
        return self

    def get_publish_data_as_private(self) -> bool:
        return self.get_proto().publish_data_as_private

    def set_publish_data_as_private(self, publish_data_as_private: bool) -> 'AppSettings':
        redvox.api1000.common.typing.check_type(publish_data_as_private, [bool])
        self.get_proto().publish_data_as_private = publish_data_as_private
        return self

    def get_scramble_audio_data(self) -> bool:
        return self.get_proto().scramble_audio_data

    def set_scramble_audio_data(self, scramble_audio_data: bool) -> 'AppSettings':
        redvox.api1000.common.typing.check_type(scramble_audio_data, [bool])
        self.get_proto().scramble_audio_data = scramble_audio_data
        return self

    def get_provide_backfill(self) -> bool:
        return self.get_proto().provide_backfill

    def set_provide_backfill(self, provide_backfill: bool) -> 'AppSettings':
        redvox.api1000.common.typing.check_type(provide_backfill, [bool])
        self.get_proto().provide_backfill = provide_backfill
        return self

    def get_remove_sensor_dc_offset(self) -> bool:
        return self.get_proto().remove_sensor_dc_offset

    def set_remove_sensor_dc_offset(self, remove_sensor_dc_offset: bool) -> 'AppSettings':
        redvox.api1000.common.typing.check_type(remove_sensor_dc_offset, [bool])
        self.get_proto().remove_sensor_dc_offset = remove_sensor_dc_offset
        return self

    def get_use_custom_time_sync_server(self) -> bool:
        return self.get_proto().use_custom_time_sync_server

    def set_use_custom_time_sync_server(self, use_custom_time_sync_server: bool) -> 'AppSettings':
        redvox.api1000.common.typing.check_type(use_custom_time_sync_server, [bool])
        self.get_proto().use_custom_time_sync_server = use_custom_time_sync_server
        return self

    def get_time_sync_server_url(self) -> str:
        return self.get_proto().time_sync_server_url

    def set_time_sync_server_url(self, time_sync_server_url: str) -> 'AppSettings':
        redvox.api1000.common.typing.check_type(time_sync_server_url, [str])
        self.get_proto().time_sync_server_url = time_sync_server_url
        return self

    def get_use_custom_data_server(self) -> bool:
        return self.get_proto().use_custom_data_server

    def set_use_custom_data_server(self, use_custom_data_server: bool) -> 'AppSettings':
        redvox.api1000.common.typing.check_type(use_custom_data_server, [bool])
        self.get_proto().use_custom_data_server = use_custom_data_server
        return self

    def get_data_server_url(self) -> str:
        return self.get_proto().data_server_url

    def set_data_server_url(self, data_server_url: str) -> 'AppSettings':
        redvox.api1000.common.typing.check_type(data_server_url, [str])
        self.get_proto().data_server_url = data_server_url
        return self

    def get_auto_delete_data_files(self) -> bool:
        return self.get_proto().auto_delete_data_files

    def set_auto_delete_data_files(self, auto_delete_data_files: bool) -> 'AppSettings':
        redvox.api1000.common.typing.check_type(auto_delete_data_files, [bool])
        self.get_proto().auto_delete_data_files = auto_delete_data_files
        return self

    def get_storage_space_allowance(self) -> float:
        return self.get_proto().storage_space_allowance

    def set_storage_space_allowance(self, storage_space_allowance: float) -> 'AppSettings':
        redvox.api1000.common.typing.check_type(storage_space_allowance, [int, float])

        self.get_proto().storage_space_allowance = storage_space_allowance
        return self

    def get_use_sd_card_for_data_storage(self) -> bool:
        return self.get_proto().use_sd_card_for_data_storage

    def set_use_sd_card_for_data_storage(self, use_sd_card_for_data_storage: bool) -> 'AppSettings':
        redvox.api1000.common.typing.check_type(use_sd_card_for_data_storage, [bool])
        self.get_proto().use_sd_card_for_data_storage = use_sd_card_for_data_storage
        return self

    def get_use_location_services(self) -> bool:
        return self.get_proto().use_location_services

    def set_use_location_services(self, use_location_services: bool) -> 'AppSettings':
        redvox.api1000.common.typing.check_type(use_location_services, [bool])
        self.get_proto().use_location_services = use_location_services
        return self

    def get_use_latitude(self) -> float:
        return self.get_proto().use_latitude

    def set_use_latitude(self, use_latitude: float) -> 'AppSettings':
        redvox.api1000.common.typing.check_type(use_latitude, [int, float])

        self.get_proto().use_latitude = use_latitude
        return self

    def get_use_longitude(self) -> float:
        return self.get_proto().use_longitude

    def set_use_longitude(self, use_longitude: float) -> 'AppSettings':
        redvox.api1000.common.typing.check_type(use_longitude, [int, float])

        self.get_proto().use_longitude = use_longitude
        return self

    def get_use_altitude(self) -> float:
        return self.get_proto().use_altitude

    def set_use_altitude(self, use_altitude: float) -> 'AppSettings':
        redvox.api1000.common.typing.check_type(use_altitude, [int, float])

        self.get_proto().use_altitude = use_altitude
        return self


def validate_app_settings(app: AppSettings) -> List[str]:
    errors_list = []
    if app.get_audio_sampling_rate() not in AudioSamplingRate:
        errors_list.append("App settings audio sample rate is not a valid sample rate")
    if app.get_station_id() == "":
        errors_list.append("App settings station id is missing")
    return errors_list


class NetworkType(enum.Enum):
    UNKNOWN_NETWORK: int = 0
    NO_NETWORK: int = 1
    WIFI: int = 2
    CELLULAR: int = 3
    WIRED: int = 4

    @staticmethod
    def from_proto(
            network_type: redvox_api_m_pb2.RedvoxPacketM.StationInformation.StationMetrics.NetworkType) -> 'NetworkType':
        return NetworkType(network_type)

    def into_proto(self) -> redvox_api_m_pb2.RedvoxPacketM.StationInformation.StationMetrics.NetworkType:
        return redvox_api_m_pb2.RedvoxPacketM.StationInformation.StationMetrics.NetworkType.Value(self.name)


class WifiWakeLock(enum.Enum):
    NONE: int = 0
    HIGH_PERF: int = 1
    LOW_LATENCY: int = 2
    OTHER: int = 3

    @staticmethod
    def from_proto(
            wifi_wake_lock: redvox_api_m_pb2.RedvoxPacketM.StationInformation.StationMetrics.WifiWakeLock) -> 'WifiWakeLock':
        return WifiWakeLock(wifi_wake_lock)

    def into_proto(self) -> redvox_api_m_pb2.RedvoxPacketM.StationInformation.StationMetrics.WifiWakeLock:
        return redvox_api_m_pb2.RedvoxPacketM.StationInformation.StationMetrics.WifiWakeLock.Value(self.name)


class CellServiceState(enum.Enum):
    UNKNOWN: int = 0
    EMERGENCY: int = 1
    NOMINAL: int = 2
    OUT_OF_SERVICE: int = 3
    POWER_OFF: int = 4

    @staticmethod
    def from_proto(
            cell_service_state: redvox_api_m_pb2.RedvoxPacketM.StationInformation.StationMetrics.CellServiceState) -> 'CellServiceState':
        return CellServiceState(cell_service_state)

    def into_proto(self) -> redvox_api_m_pb2.RedvoxPacketM.StationInformation.StationMetrics.CellServiceState:
        return redvox_api_m_pb2.RedvoxPacketM.StationInformation.StationMetrics.CellServiceState.Value(self.name)


class PowerState(enum.Enum):
    UNKNOWN_POWER_STATE: int = 0
    UNPLUGGED: int = 1
    CHARGING: int = 2
    CHARGED: int = 3

    @staticmethod
    def from_proto(
            power_state: redvox_api_m_pb2.RedvoxPacketM.StationInformation.StationMetrics.PowerState) -> 'PowerState':
        return PowerState(power_state)

    def into_proto(self) -> redvox_api_m_pb2.RedvoxPacketM.StationInformation.StationMetrics.PowerState:
        return redvox_api_m_pb2.RedvoxPacketM.StationInformation.StationMetrics.PowerState.Value(self.name)


class StationMetrics(
    redvox.api1000.common.generic.ProtoBase[redvox_api_m_pb2.RedvoxPacketM.StationInformation.StationMetrics]):
    def __init__(self, station_metrics_proto: redvox_api_m_pb2.RedvoxPacketM.StationInformation.StationMetrics):
        super().__init__(station_metrics_proto)
        self._timestamps = common.TimingPayload(station_metrics_proto.timestamps).set_default_unit()
        self._network_type: redvox.api1000.common.generic.ProtoRepeatedMessage = redvox.api1000.common.generic.ProtoRepeatedMessage(
            station_metrics_proto,
            station_metrics_proto.network_type,
            _NETWORK_TYPE_FIELD_NAME,
            NetworkType.from_proto,
            NetworkType.into_proto
        )
        self._cell_service_state: redvox.api1000.common.generic.ProtoRepeatedMessage = redvox.api1000.common.generic.ProtoRepeatedMessage(
            station_metrics_proto,
            station_metrics_proto.cell_service_state,
            _CELL_SERVICE_STATE_FIELD_NAME,
            CellServiceState.from_proto,
            CellServiceState.into_proto
        )
        self._network_strength: common.SamplePayload = common.SamplePayload(station_metrics_proto.network_strength)\
            .set_unit(common.Unit.DECIBEL)
        self._temperature: common.SamplePayload = common.SamplePayload(station_metrics_proto.temperature)\
            .set_unit(common.Unit.DEGREES_CELSIUS)
        self._battery: common.SamplePayload = common.SamplePayload(station_metrics_proto.battery)\
            .set_unit(common.Unit.PERCENTAGE)
        self._battery_current: common.SamplePayload = common.SamplePayload(station_metrics_proto.battery_current)\
            .set_unit(common.Unit.MICROAMPERES)
        self._available_ram: common.SamplePayload = common.SamplePayload(station_metrics_proto.available_ram)\
            .set_unit(common.Unit.BYTE)
        self._available_disk: common.SamplePayload = common.SamplePayload(station_metrics_proto.available_disk) \
            .set_unit(common.Unit.BYTE)
        self._cpu_utilization: common.SamplePayload = common.SamplePayload(station_metrics_proto.cpu_utilization)\
            .set_unit(common.Unit.PERCENTAGE)
        self._power_state: redvox.api1000.common.generic.ProtoRepeatedMessage = redvox.api1000.common.generic.ProtoRepeatedMessage(
            station_metrics_proto,
            station_metrics_proto.power_state,
            _POWER_STATE_FIELD_NAME,
            PowerState.from_proto,
            PowerState.into_proto
        )

    @staticmethod
    def new() -> 'StationMetrics':
        return StationMetrics(redvox_api_m_pb2.RedvoxPacketM.StationInformation.StationMetrics())

    def get_timestamps(self) -> common.TimingPayload:
        return self._timestamps

    def get_network_type(self) -> redvox.api1000.common.generic.ProtoRepeatedMessage:
        return self._network_type

    def get_cell_service_state(self) -> redvox.api1000.common.generic.ProtoRepeatedMessage:
        return self._cell_service_state

    def get_network_strength(self) -> common.SamplePayload:
        return self._network_strength

    def get_temperature(self) -> common.SamplePayload:
        return self._temperature

    def get_battery(self) -> common.SamplePayload:
        return self._battery

    def get_battery_current(self) -> common.SamplePayload:
        return self._battery_current

    def get_available_ram(self) -> common.SamplePayload:
        return self._available_ram

    def get_available_disk(self) -> common.SamplePayload:
        return self._available_disk

    def get_cpu_utilization(self) -> common.SamplePayload:
        return self._cpu_utilization

    def get_power_state(self) -> redvox.api1000.common.generic.ProtoRepeatedMessage:
        return self._power_state

    def get_wifi_wake_loc(self) -> WifiWakeLock:
        return WifiWakeLock(self.get_proto().wifi_wake_lock)

    def set_wifi_wake_loc(self, wifi_wake_loc: WifiWakeLock) -> 'StationMetrics':
        redvox.api1000.common.typing.check_type(wifi_wake_loc, [WifiWakeLock])
        self.get_proto().wifi_wake_loc = redvox_api_m_pb2.RedvoxPacketM.StationInformation.StationMetrics.WifiWakeLock.Value(
            wifi_wake_loc.name)
        return self


class ServiceUrls(
    redvox.api1000.common.generic.ProtoBase[redvox_api_m_pb2.RedvoxPacketM.StationInformation.ServiceUrls]):
    def __init__(self, service_urls_proto: redvox_api_m_pb2.RedvoxPacketM.StationInformation.ServiceUrls):
        super().__init__(service_urls_proto)

    @staticmethod
    def new() -> 'ServiceUrls':
        return ServiceUrls(redvox_api_m_pb2.RedvoxPacketM.StationInformation.ServiceUrls())

    def get_auth_server(self) -> str:
        return self.get_proto().auth_server

    def set_auth_server(self, _auth_server: str) -> 'ServiceUrls':
        redvox.api1000.common.typing.check_type(_auth_server, [str])
        self.get_proto().auth_server = _auth_server
        return self

    def get_synch_server(self) -> str:
        return self.get_proto().synch_server

    def set_synch_server(self, _synch_server: str) -> 'ServiceUrls':
        redvox.api1000.common.typing.check_type(_synch_server, [str])
        self.get_proto().synch_server = _synch_server
        return self

    def get_acquisition_server(self) -> str:
        return self.get_proto().acquisition_server

    def set_acquisition_server(self, _acquisition_server: str) -> 'ServiceUrls':
        redvox.api1000.common.typing.check_type(_acquisition_server, [str])
        self.get_proto().acquisition_server = _acquisition_server
        return self


def validate_station_metrics(station_metrics: StationMetrics) -> List[str]:
    # only check if timestamps are valid right now
    # todo: determine if other stuff needs to be validated as well
    return common.validate_timing_payload(station_metrics.get_timestamps())


class OsType(enum.Enum):
    UNKNOWN_OS: int = 0
    ANDROID: int = 1
    IOS: int = 2
    OSX: int = 3
    LINUX: int = 4
    WINDOWS: int = 5

    @staticmethod
    def from_proto(os_type: redvox_api_m_pb2.RedvoxPacketM.StationInformation.OsType) -> 'OsType':
        return OsType(os_type)

    def into_proto(self) -> redvox_api_m_pb2.RedvoxPacketM.StationInformation.OsType:
        return redvox_api_m_pb2.RedvoxPacketM.StationInformation.OsType.Value(self.name)


class StationInformation(
    redvox.api1000.common.generic.ProtoBase[redvox_api_m_pb2.RedvoxPacketM.StationInformation]):
    def __init__(self, station_information_proto: redvox_api_m_pb2.RedvoxPacketM.StationInformation):
        super().__init__(station_information_proto)
        self._app_settings: AppSettings = AppSettings(station_information_proto.app_settings)
        self._station_metrics: StationMetrics = StationMetrics(station_information_proto.station_metrics)
        self._service_urls: ServiceUrls = ServiceUrls(station_information_proto.service_urls)

    @staticmethod
    def new() -> 'StationInformation':
        return StationInformation(redvox_api_m_pb2.RedvoxPacketM.StationInformation())

    def get_id(self) -> str:
        return self.get_proto().id

    def set_id(self, _id: str) -> 'StationInformation':
        redvox.api1000.common.typing.check_type(_id, [str])
        self.get_proto().id = _id
        return self

    def get_uuid(self) -> str:
        return self.get_proto().uuid

    def set_uuid(self, uuid: str) -> 'StationInformation':
        redvox.api1000.common.typing.check_type(uuid, [str])
        self.get_proto().uuid = uuid
        return self

    def get_description(self) -> str:
        return self.get_proto().description

    def set_description(self, description: str) -> 'StationInformation':
        redvox.api1000.common.typing.check_type(description, [str])
        self.get_proto().description = description
        return self

    def get_auth_id(self) -> str:
        return self.get_proto().auth_id

    def set_auth_id(self, auth_id: str) -> 'StationInformation':
        redvox.api1000.common.typing.check_type(auth_id, [str])
        self.get_proto().auth_id = auth_id
        return self

    def get_make(self) -> str:
        return self.get_proto().make

    def set_make(self, make: str) -> 'StationInformation':
        redvox.api1000.common.typing.check_type(make, [str])
        self.get_proto().make = make
        return self

    def get_model(self) -> str:
        return self.get_proto().model

    def set_model(self, model: str) -> 'StationInformation':
        redvox.api1000.common.typing.check_type(model, [str])
        self.get_proto().model = model
        return self

    def get_os(self) -> OsType:
        return OsType(self.get_proto().os)

    def set_os(self, os: OsType) -> 'StationInformation':
        redvox.api1000.common.typing.check_type(os, [OsType])
        self.get_proto().os = redvox_api_m_pb2.RedvoxPacketM.StationInformation.OsType.Value(os.name)
        return self

    def get_os_version(self) -> str:
        return self.get_proto().os_version

    def set_os_version(self, os_version: str) -> 'StationInformation':
        redvox.api1000.common.typing.check_type(os_version, [str])
        self.get_proto().os_version = os_version
        return self

    def get_app_version(self) -> str:
        return self.get_proto().app_version

    def set_app_version(self, app_version: str) -> 'StationInformation':
        redvox.api1000.common.typing.check_type(app_version, [str])
        self.get_proto().app_version = app_version
        return self

    def get_is_private(self) -> bool:
        return self.get_proto().is_private

    def set_is_private(self, is_private: bool) -> 'StationInformation':
        redvox.api1000.common.typing.check_type(is_private, [bool])
        self.get_proto().is_private = is_private
        return self

    def get_app_settings(self) -> AppSettings:
        return self._app_settings

    def get_station_metrics(self) -> StationMetrics:
        return self._station_metrics

    def get_service_urls(self) -> ServiceUrls:
        return self._service_urls


def validate_station_information(station_info: StationInformation) -> List[str]:
    errors_list = validate_app_settings(station_info.get_app_settings())
    errors_list.extend(validate_station_metrics(station_info.get_station_metrics()))
    if station_info.get_id() == "":
        errors_list.append("Station information station id missing")
    if station_info.get_uuid() == "":
        errors_list.append("Station information station uuid missing")
    return errors_list
