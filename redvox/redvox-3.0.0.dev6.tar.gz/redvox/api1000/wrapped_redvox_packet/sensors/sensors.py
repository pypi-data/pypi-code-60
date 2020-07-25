"""
This module encapsulates available sensor types.
"""

from typing import Optional, List

import redvox.api1000.common.common as common
import redvox.api1000.common.typing
import redvox.api1000.proto.redvox_api_m_pb2 as redvox_api_m_pb2
import redvox.api1000.common.generic
import redvox.api1000.wrapped_redvox_packet.sensors.audio as audio
import redvox.api1000.wrapped_redvox_packet.sensors.image as image
import redvox.api1000.wrapped_redvox_packet.sensors.location as location
import redvox.api1000.wrapped_redvox_packet.sensors.single as single
import redvox.api1000.wrapped_redvox_packet.sensors.xyz as xyz

_ACCELEROMETER_FIELD_NAME: str = "accelerometer"
_AMBIENT_TEMPERATURE_FIELD_NAME: str = "ambient_temperature"
_AUDIO_FIELD_NAME: str = "audio"
_COMPRESSED_AUDIO_FIELD_NAME: str = "compressed_audio"
_GRAVITY_FIELD_NAME: str = "gravity"
_GYROSCOPE_FIELD_NAME: str = "gyroscope"
_IMAGE_FIELD_NAME: str = "image"
_LIGHT_FIELD_NAME: str = "light"
_LINEAR_ACCELERATION_FIELD_NAME: str = "linear_acceleration"
_LOCATION_FIELD_NAME: str = "location"
_MAGNETOMETER_FIELD_NAME: str = "magnetometer"
_ORIENTATION_FIELD_NAME: str = "orientation"
_PRESSURE_FIELD_NAME: str = "pressure"
_PROXIMITY_FIELD_NAME: str = "proximity"
_RELATIVE_HUMIDITY_FIELD_NAME: str = "relative_humidity"
_ROTATION_VECTOR: str = "rotation_vector"


class Sensors(redvox.api1000.common.generic.ProtoBase[redvox_api_m_pb2.RedvoxPacketM.Sensors]):
    def __init__(self, sensors_proto: redvox_api_m_pb2.RedvoxPacketM.Sensors):
        super().__init__(sensors_proto)
        self._accelerometer: xyz.Xyz = xyz.Xyz(sensors_proto.accelerometer)
        self._ambient_temperature: single.Single = single.Single(sensors_proto.ambient_temperature)
        self._audio: audio.Audio = audio.Audio(sensors_proto.audio)
        self._compressed_audio: audio.CompressedAudio = audio.CompressedAudio(sensors_proto.compressed_audio)
        self._gravity: xyz.Xyz = xyz.Xyz(sensors_proto.gravity)
        self._gyroscope: xyz.Xyz = xyz.Xyz(sensors_proto.gyroscope)
        self._image: image.Image = image.Image(sensors_proto.image)
        self._light: single.Single = single.Single(sensors_proto.light)
        self._linear_acceleration: xyz.Xyz = xyz.Xyz(sensors_proto.linear_acceleration)
        self._location: location.Location = location.Location(sensors_proto.location)
        self._magnetometer: xyz.Xyz = xyz.Xyz(sensors_proto.magnetometer)
        self._orientation: xyz.Xyz = xyz.Xyz(sensors_proto.orientation)
        self._pressure: single.Single = single.Single(sensors_proto.pressure)
        self._proximity: single.Single = single.Single(sensors_proto.proximity)
        self._relative_humidity: single.Single = single.Single(sensors_proto.relative_humidity)
        self._rotation_vector: xyz.Xyz = xyz.Xyz(sensors_proto.rotation_vector)

    @staticmethod
    def new() -> 'Sensors':
        return Sensors(redvox_api_m_pb2.RedvoxPacketM.Sensors())

    def has_accelerometer(self) -> bool:
        return self.get_proto().HasField(_ACCELEROMETER_FIELD_NAME)

    def get_accelerometer(self) -> xyz.Xyz:
        return self._accelerometer if self.has_accelerometer() else None
        # return self._accelerometer

    def new_accelerometer(self) -> xyz.Xyz:
        self.remove_accelerometer()
        self.get_proto().accelerometer.SetInParent()
        self._accelerometer = xyz.Xyz(self.get_proto().accelerometer)
        self._accelerometer.get_timestamps().set_default_unit()
        self._accelerometer.set_unit_xyz(common.Unit.METERS_PER_SECOND_SQUARED)
        return self._accelerometer

    def set_accelerometer(self, accelerometer: xyz.Xyz) -> 'Sensors':
        redvox.api1000.common.typing.check_type(accelerometer, [xyz.Xyz])
        self.get_proto().accelerometer.CopyFrom(accelerometer.get_proto())
        return self

    def remove_accelerometer(self) -> 'Sensors':
        self.get_proto().ClearField(_ACCELEROMETER_FIELD_NAME)
        return self

    def has_ambient_temperature(self) -> bool:
        return self.get_proto().HasField(_AMBIENT_TEMPERATURE_FIELD_NAME)

    def get_ambient_temperature(self) -> Optional[single.Single]:
        return self._ambient_temperature if self.has_ambient_temperature() else None

    def new_ambient_temperature(self) -> single.Single:
        self.remove_ambient_temperature()
        self.get_proto().ambient_temperature.SetInParent()
        self._ambient_temperature = single.Single(self.get_proto().ambient_temperature)
        self._ambient_temperature.get_timestamps().set_default_unit()
        self._ambient_temperature.get_samples().set_unit(common.Unit.DEGREES_CELSIUS)
        return self._ambient_temperature

    def set_ambient_temperature(self, ambient_temperature: single.Single) -> 'Sensors':
        redvox.api1000.common.typing.check_type(ambient_temperature, [single.Single])
        self.get_proto().ambient_temperature.CopyFrom(ambient_temperature.get_proto())
        return self

    def remove_ambient_temperature(self) -> 'Sensors':
        self.get_proto().ClearField(_AMBIENT_TEMPERATURE_FIELD_NAME)
        return self

    def has_audio(self) -> bool:
        return self.get_proto().HasField(_AUDIO_FIELD_NAME)

    def get_audio(self) -> Optional[audio.Audio]:
        return self._audio if self.has_audio() else None

    def new_audio(self) -> audio.Audio:
        self.remove_audio()
        self.get_proto().audio.SetInParent()
        self._audio = audio.Audio(self.get_proto().audio)
        self._audio.get_samples().set_unit(common.Unit.LSB_PLUS_MINUS_COUNTS)
        return self._audio

    def set_audio(self, _audio: audio.Audio) -> 'Sensors':
        redvox.api1000.common.typing.check_type(_audio, [audio.Audio])
        self.get_proto().audio.CopyFrom(_audio.get_proto())
        return self

    def remove_audio(self) -> 'Sensors':
        self.get_proto().ClearField(_AUDIO_FIELD_NAME)
        return self

    def has_compress_audio(self) -> bool:
        return self.get_proto().HasField(_COMPRESSED_AUDIO_FIELD_NAME)

    def get_compressed_audio(self) -> Optional[audio.CompressedAudio]:
        return self._compressed_audio if self.has_compress_audio() else None

    def new_compressed_audio(self) -> audio.CompressedAudio:
        self.remove_compressed_audio()
        self.get_proto().compressed_audio.SetInParent()
        self._compressed_audio = audio.CompressedAudio(self.get_proto().compressed_audio)
        return self._compressed_audio

    def set_compressed_audio(self, compressed_audio: audio.CompressedAudio) -> 'Sensors':
        redvox.api1000.common.typing.check_type(compressed_audio, [audio.Audio])
        self.get_proto().audio.CopyFrom(compressed_audio.get_proto())
        return self

    def remove_compressed_audio(self) -> 'Sensors':
        self.get_proto().ClearField(_COMPRESSED_AUDIO_FIELD_NAME)
        return self

    def has_gravity(self) -> bool:
        return self.get_proto().HasField(_GRAVITY_FIELD_NAME)

    def get_gravity(self) -> Optional[xyz.Xyz]:
        return self._gravity if self.has_gravity() else None

    def new_gravity(self) -> xyz.Xyz:
        self.remove_gravity()
        self.get_proto().gravity.SetInParent()
        self._gravity = xyz.Xyz(self.get_proto().gravity)
        self._gravity.get_timestamps().set_default_unit()
        self._gravity.set_unit_xyz(common.Unit.METERS_PER_SECOND_SQUARED)
        return self._gravity

    def set_gravity(self, gravity: xyz.Xyz) -> 'Sensors':
        redvox.api1000.common.typing.check_type(gravity, [xyz.Xyz])
        self.get_proto().gravity.CopyFrom(gravity.get_proto())
        return self

    def remove_gravity(self) -> 'Sensors':
        self.get_proto().ClearField(_GRAVITY_FIELD_NAME)
        return self

    def has_gyroscope(self) -> bool:
        return self.get_proto().HasField(_GYROSCOPE_FIELD_NAME)

    def get_gyroscope(self) -> Optional[xyz.Xyz]:
        return self._gyroscope if self.has_gyroscope() else None

    def new_gyroscope(self) -> xyz.Xyz:
        self.remove_gyroscope()
        self.get_proto().gyroscope.SetInParent()
        self._gyroscope = xyz.Xyz(self.get_proto().gyroscope)
        self._gyroscope.get_timestamps().set_default_unit()
        self._gyroscope.set_unit_xyz(common.Unit.RADIANS_PER_SECOND)
        return self._gyroscope

    def set_gyroscope(self, gyroscope: xyz.Xyz) -> 'Sensors':
        redvox.api1000.common.typing.check_type(gyroscope, [xyz.Xyz])
        self.get_proto().gyroscope.CopyFrom(gyroscope.get_proto())
        return self

    def remove_gyroscope(self) -> 'Sensors':
        self.get_proto().ClearField(_GYROSCOPE_FIELD_NAME)
        return self

    def has_image(self) -> bool:
        return self.get_proto().HasField(_IMAGE_FIELD_NAME)

    def get_image(self) -> Optional[image.Image]:
        return self._image if self.has_image() else None

    def new_image(self) -> image.Image:
        self.remove_image()
        self.get_proto().image.SetInParent()
        self._image = image.Image(self.get_proto().image)
        self._image.set_image_codec(image.ImageCodec.PNG)
        return self._image

    def set_image(self, _image: image.Image) -> 'Sensors':
        redvox.api1000.common.typing.check_type(_image, [image.Image])
        self.get_proto().image.CopyFrom(_image.get_proto())
        return self

    def remove_image(self) -> 'Sensors':
        self.get_proto().ClearField(_IMAGE_FIELD_NAME)
        return self

    def has_light(self) -> bool:
        return self.get_proto().HasField(_LIGHT_FIELD_NAME)

    def get_light(self) -> Optional[single.Single]:
        return self._light if self.has_light() else None

    def new_light(self) -> single.Single:
        self.remove_light()
        self.get_proto().light.SetInParent()
        self._light = single.Single(self.get_proto().light)
        self._light.get_timestamps().set_default_unit()
        self._light.get_samples().set_unit(common.Unit.LUX)
        return self._light

    def set_light(self, light: single.Single) -> 'Sensors':
        redvox.api1000.common.typing.check_type(light, [single.Single])
        self.get_proto().light.CopyFrom(light.get_proto())
        return self

    def remove_light(self) -> 'Sensors':
        self.get_proto().ClearField(_LIGHT_FIELD_NAME)
        return self

    def has_linear_acceleration(self) -> bool:
        return self.get_proto().HasField(_LINEAR_ACCELERATION_FIELD_NAME)

    def get_linear_acceleration(self) -> Optional[xyz.Xyz]:
        return self._linear_acceleration if self.has_linear_acceleration() else None

    def new_linear_acceleration(self) -> xyz.Xyz:
        self.remove_linear_acceleration()
        self.get_proto().linear_acceleration.SetInParent()
        self._linear_acceleration = xyz.Xyz(self.get_proto().linear_acceleration)
        self._linear_acceleration.get_timestamps().set_default_unit()
        self._linear_acceleration.set_unit_xyz(common.Unit.METERS_PER_SECOND_SQUARED)
        return self._linear_acceleration

    def set_linear_acceleration(self, linear_acceleration: xyz.Xyz) -> 'Sensors':
        redvox.api1000.common.typing.check_type(linear_acceleration, [xyz.Xyz])
        self.get_proto().linear_acceleration.CopyFrom(linear_acceleration.get_proto())
        return self

    def remove_linear_acceleration(self) -> 'Sensors':
        self.get_proto().ClearField(_LINEAR_ACCELERATION_FIELD_NAME)
        return self

    def has_location(self) -> bool:
        return self.get_proto().HasField(_LOCATION_FIELD_NAME)

    def get_location(self) -> Optional[location.Location]:
        return self._location if self.has_location() else None

    def new_location(self) -> location.Location:
        self.remove_location()
        self.get_proto().location.SetInParent()
        self._location = location.Location(self.get_proto().location)
        self._location.get_timestamps().set_default_unit()
        self._location.get_latitude_samples().set_unit(common.Unit.DECIMAL_DEGREES)
        self._location.get_longitude_samples().set_unit(common.Unit.DECIMAL_DEGREES)
        self._location.get_altitude_samples().set_unit(common.Unit.METERS)
        self._location.get_speed_samples().set_unit(common.Unit.METERS_PER_SECOND)
        self._location.get_bearing_samples().set_unit(common.Unit.DECIMAL_DEGREES)
        self._location.get_horizontal_accuracy_samples().set_unit(common.Unit.METERS)
        self._location.get_vertical_accuracy_samples().set_unit(common.Unit.METERS)
        self._location.get_speed_accuracy_samples().set_unit(common.Unit.METERS_PER_SECOND)
        self._location.get_bearing_accuracy_samples().set_unit(common.Unit.DECIMAL_DEGREES)
        return self._location

    def set_location(self, _location: location.Location) -> 'Sensors':
        redvox.api1000.common.typing.check_type(_location, [location.Location])
        self.get_proto().location.CopyFrom(_location.get_proto())
        return self

    def remove_location(self) -> 'Sensors':
        self.get_proto().ClearField(_LOCATION_FIELD_NAME)
        return self

    def has_magnetometer(self) -> bool:
        return self.get_proto().HasField(_MAGNETOMETER_FIELD_NAME)

    def get_magnetometer(self) -> Optional[xyz.Xyz]:
        return self._magnetometer if self.has_magnetometer() else None

    def new_magnetometer(self) -> xyz.Xyz:
        self.remove_magnetometer()
        self.get_proto().magnetometer.SetInParent()
        self._magnetometer = xyz.Xyz(self.get_proto().magnetometer)
        self._magnetometer.get_timestamps().set_default_unit()
        self._magnetometer.set_unit_xyz(common.Unit.MICROTESLA)
        return self._magnetometer

    def set_magnetometer(self, magnetometer: xyz.Xyz) -> 'Sensors':
        redvox.api1000.common.typing.check_type(magnetometer, [xyz.Xyz])
        self.get_proto().magnetometer.CopyFrom(magnetometer.get_proto())
        return self

    def remove_magnetometer(self) -> 'Sensors':
        self.get_proto().ClearField(_MAGNETOMETER_FIELD_NAME)
        return self

    def has_orientation(self) -> bool:
        return self.get_proto().HasField(_ORIENTATION_FIELD_NAME)

    def get_orientation(self) -> Optional[xyz.Xyz]:
        return self._orientation if self.has_orientation() else None

    def new_orientation(self) -> xyz.Xyz:
        self.remove_orientation()
        self.get_proto().orientation.SetInParent()
        self._orientation = xyz.Xyz(self.get_proto().orientation)
        self._orientation.get_timestamps().set_default_unit()
        self._orientation.set_unit_xyz(common.Unit.RADIANS)
        return self._orientation

    def set_orientation(self, orientation: xyz.Xyz) -> 'Sensors':
        redvox.api1000.common.typing.check_type(orientation, [xyz.Xyz])
        self.get_proto().orientation.CopyFrom(orientation.get_proto())
        return self

    def remove_orientation(self) -> 'Sensors':
        self.get_proto().ClearField(_ORIENTATION_FIELD_NAME)
        return self

    def has_pressure(self) -> bool:
        return self.get_proto().HasField(_PRESSURE_FIELD_NAME)

    def get_pressure(self) -> Optional[single.Single]:
        return self._pressure if self.has_pressure() else None

    def new_pressure(self) -> single.Single:
        self.remove_pressure()
        self.get_proto().pressure.SetInParent()
        self._pressure = single.Single(self.get_proto().pressure)
        self._pressure.get_timestamps().set_default_unit()
        self._pressure.get_samples().set_unit(common.Unit.KILOPASCAL)
        return self._pressure

    def set_pressure(self, pressure: single.Single) -> 'Sensors':
        redvox.api1000.common.typing.check_type(pressure, [single.Single])
        self.get_proto().pressure.CopyFrom(pressure.get_proto())
        return self

    def remove_pressure(self) -> 'Sensors':
        self.get_proto().ClearField(_PRESSURE_FIELD_NAME)
        return self

    def has_proximity(self) -> bool:
        return self.get_proto().HasField(_PROXIMITY_FIELD_NAME)

    def get_proximity(self) -> Optional[single.Single]:
        return self._proximity if self.has_proximity() else None

    def new_proximity(self) -> single.Single:
        self.remove_proximity()
        self.get_proto().proximity.SetInParent()
        self._proximity = single.Single(self.get_proto().proximity)
        self._proximity.get_timestamps().set_default_unit()
        self._proximity.get_samples().set_unit(common.Unit.CENTIMETERS)
        return self._proximity

    def set_proximity(self, proximity: single.Single) -> 'Sensors':
        redvox.api1000.common.typing.check_type(proximity, [single.Single])
        self.get_proto().proximity.CopyFrom(proximity.get_proto())
        return self

    def remove_proximity(self) -> 'Sensors':
        self.get_proto().ClearField(_PROXIMITY_FIELD_NAME)
        return self

    def has_relative_humidity(self) -> bool:
        return self.get_proto().HasField(_RELATIVE_HUMIDITY_FIELD_NAME)

    def get_relative_humidity(self) -> Optional[single.Single]:
        return self._relative_humidity if self.has_relative_humidity() else None

    def new_relative_humidity(self) -> single.Single:
        self.remove_relative_humidity()
        self.get_proto().relative_humidity.SetInParent()
        self._relative_humidity = single.Single(self.get_proto().relative_humidity)
        self._relative_humidity.get_timestamps().set_default_unit()
        self._relative_humidity.get_samples().set_unit(common.Unit.PERCENTAGE)
        return self._relative_humidity

    def set_relative_humidity(self, relative_humidity: single.Single) -> 'Sensors':
        redvox.api1000.common.typing.check_type(relative_humidity, [single.Single])
        self.get_proto().relative_humidity.CopyFrom(relative_humidity.get_proto())
        return self

    def remove_relative_humidity(self) -> 'Sensors':
        self.get_proto().ClearField(_RELATIVE_HUMIDITY_FIELD_NAME)
        return self

    def has_rotation_vector(self) -> bool:
        return self.get_proto().HasField(_ROTATION_VECTOR)

    def get_rotation_vector(self) -> Optional[xyz.Xyz]:
        return self._rotation_vector if self.has_rotation_vector() else None

    def new_rotation_vector(self) -> xyz.Xyz:
        self.remove_rotation_vector()
        self.get_proto().rotation_vector.SetInParent()
        self._rotation_vector = xyz.Xyz(self.get_proto().rotation_vector)
        self._rotation_vector.get_timestamps().set_default_unit()
        self._rotation_vector.set_unit_xyz(common.Unit.UNITLESS)
        return self._rotation_vector

    def set_rotation_vector(self, rotation_vector: xyz.Xyz) -> 'Sensors':
        redvox.api1000.common.typing.check_type(rotation_vector, [xyz.Xyz])
        self.get_proto().rotation_vector.CopyFrom(rotation_vector.get_proto())
        return self

    def remove_rotation_vector(self) -> 'Sensors':
        self.get_proto().ClearField(_ROTATION_VECTOR)
        return self


def validate_sensors(sensors_list: Sensors) -> List[str]:
    # audio is the only sensor that every packet must have
    errors_list = []
    if not sensors_list.has_audio() and not sensors_list.has_compress_audio():
        errors_list.append("Sensors list missing audio sensor")
    else:
        if sensors_list.has_audio():
            errors_list.extend(audio.validate_audio(sensors_list.get_audio()))
        if sensors_list.has_compress_audio():
            errors_list.extend(audio.validate_compress_audio(sensors_list.get_compressed_audio()))
    if sensors_list.has_accelerometer():
        errors_list.extend(xyz.validate_xyz(sensors_list.get_accelerometer(), common.Unit.METERS_PER_SECOND_SQUARED))
    if sensors_list.has_ambient_temperature():
        errors_list.extend(single.validate_single(sensors_list.get_ambient_temperature(), common.Unit.DEGREES_CELSIUS))
    if sensors_list.has_gravity():
        errors_list.extend(xyz.validate_xyz(sensors_list.get_gravity(), common.Unit.METERS_PER_SECOND_SQUARED))
    if sensors_list.has_gyroscope():
        errors_list.extend(xyz.validate_xyz(sensors_list.get_gyroscope(), common.Unit.RADIANS_PER_SECOND))
    if sensors_list.has_image():
        errors_list.extend(image.validate_image(sensors_list.get_image()))
    if sensors_list.has_light():
        errors_list.extend(single.validate_single(sensors_list.get_light(), common.Unit.LUX))
    if sensors_list.has_linear_acceleration():
        errors_list.extend(xyz.validate_xyz(sensors_list.get_linear_acceleration(),
                                            common.Unit.METERS_PER_SECOND_SQUARED))
    if sensors_list.has_location():
        errors_list.extend(location.validate_location(sensors_list.get_location()))
    if sensors_list.has_magnetometer():
        errors_list.extend(xyz.validate_xyz(sensors_list.get_magnetometer(), common.Unit.MICROTESLA))
    if sensors_list.has_orientation():
        errors_list.extend(xyz.validate_xyz(sensors_list.get_orientation(), common.Unit.RADIANS))
    if sensors_list.has_pressure():
        errors_list.extend(single.validate_single(sensors_list.get_pressure(), common.Unit.KILOPASCAL))
    if sensors_list.has_proximity():
        errors_list.extend(single.validate_single(sensors_list.get_proximity(), common.Unit.CENTIMETERS))
    if sensors_list.has_relative_humidity():
        errors_list.extend(single.validate_single(sensors_list.get_relative_humidity(), common.Unit.PERCENTAGE))
    if sensors_list.has_rotation_vector():
        errors_list.extend(xyz.validate_xyz(sensors_list.get_rotation_vector(), common.Unit.UNITLESS))
    return errors_list
