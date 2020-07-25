# coding=utf-8
from ladybug.wea import Wea
from ladybug.location import Location
from ladybug.analysisperiod import AnalysisPeriod
from ladybug.epw import EPW
from ladybug.datacollection import HourlyContinuousCollection, HourlyDiscontinuousCollection

import pytest
import os


def test_from_file():
    """Test import from wea file."""
    wea_file = './tests/fixtures/wea/san_francisco_10min.wea'
    with pytest.raises(Exception):
        Wea.from_file(wea_file)  # wrong timestep

    wea = Wea.from_file(wea_file, 6)
    assert isinstance(wea.direct_normal_irradiance, HourlyContinuousCollection)
    assert isinstance(wea.diffuse_horizontal_irradiance, HourlyContinuousCollection)
    assert wea.is_annual
    assert wea.is_continuous
    assert wea.direct_normal_irradiance[45] == 69
    assert wea.diffuse_horizontal_irradiance[45] == 1
    assert wea.direct_normal_irradiance[46] == 137
    assert wea.diffuse_horizontal_irradiance[46] == 7


def test_from_file_discontinuous():
    """Test import from wea file with discontinuous data."""
    wea_file = './tests/fixtures/wea/chicago_filtered.wea'
    wea = Wea.from_file(wea_file)

    assert isinstance(wea.direct_normal_irradiance, HourlyDiscontinuousCollection)
    assert isinstance(wea.diffuse_horizontal_irradiance, HourlyDiscontinuousCollection)
    assert not wea.is_annual
    assert not wea.is_continuous
    assert len(wea) == 4427
    assert wea.datetimes[0].hour == 7


def test_from_file_daysim():
    """Test import from wea file with a shorter timestep as generated by DAYSIM."""
    wea_file = './tests/fixtures/wea/san_francisco_10min_daysim.wea'
    with pytest.raises(Exception):
        Wea.from_daysim_file(wea_file)  # wrong timestep

    wea = Wea.from_daysim_file(wea_file, 6)
    assert isinstance(wea.direct_normal_irradiance, HourlyContinuousCollection)
    assert isinstance(wea.diffuse_horizontal_irradiance, HourlyContinuousCollection)
    assert wea.direct_normal_irradiance[48] == 88
    assert wea.diffuse_horizontal_irradiance[48] == 1
    assert wea.direct_normal_irradiance[49] == 313
    assert wea.diffuse_horizontal_irradiance[49] == 3


def test_from_epw():
    """Test import from epw"""
    epw_path = './tests/fixtures/epw/chicago.epw'
    wea_from_epw = Wea.from_epw_file(epw_path)

    assert wea_from_epw.location.city == 'Chicago Ohare Intl Ap'
    assert wea_from_epw.timestep == 1
    assert wea_from_epw.direct_normal_irradiance[7] == 22
    assert wea_from_epw.direct_normal_irradiance.datetimes[7].hour == 7
    assert wea_from_epw.direct_normal_irradiance.datetimes[7].minute == 0
    assert wea_from_epw.direct_normal_irradiance[8] == 397
    assert wea_from_epw.direct_normal_irradiance.datetimes[8].hour == 8
    assert wea_from_epw.direct_normal_irradiance.datetimes[8].minute == 0
    # diffuse horizontal irradiance
    assert wea_from_epw.diffuse_horizontal_irradiance[7] == 10
    assert wea_from_epw.diffuse_horizontal_irradiance.datetimes[7].hour == 7
    assert wea_from_epw.diffuse_horizontal_irradiance.datetimes[7].minute == 0
    assert wea_from_epw.diffuse_horizontal_irradiance[8] == 47
    assert wea_from_epw.diffuse_horizontal_irradiance.datetimes[8].hour == 8
    assert wea_from_epw.diffuse_horizontal_irradiance.datetimes[8].minute == 0


def test_from_epw_fine_timestep():
    """Test import from epw"""
    epw_path = './tests/fixtures/epw/chicago.epw'
    wea_from_epw = Wea.from_epw_file(epw_path, 2)

    assert wea_from_epw.location.city == 'Chicago Ohare Intl Ap'
    assert wea_from_epw.timestep == 2
    assert wea_from_epw.direct_normal_irradiance[15] == 22
    assert wea_from_epw.direct_normal_irradiance.datetimes[15].hour == 7
    assert wea_from_epw.direct_normal_irradiance.datetimes[15].minute == 30
    assert wea_from_epw.direct_normal_irradiance[17] == 397
    assert wea_from_epw.direct_normal_irradiance.datetimes[17].hour == 8
    assert wea_from_epw.direct_normal_irradiance.datetimes[17].minute == 30


def test_from_stat():
    """Test import from stat"""
    stat_path = './tests/fixtures/stat/chicago.stat'
    wea_from_stat = Wea.from_stat_file(stat_path)

    assert wea_from_stat.location.city == 'Chicago Ohare Intl Ap'
    assert wea_from_stat.timestep == 1
    assert wea_from_stat.diffuse_horizontal_irradiance[0] == \
        pytest.approx(0, rel=1e-3)
    assert wea_from_stat.direct_normal_irradiance[0] == \
        pytest.approx(0, rel=1e-3)
    assert wea_from_stat.diffuse_horizontal_irradiance[12] == \
        pytest.approx(87.44171, rel=1e-3)
    assert wea_from_stat.direct_normal_irradiance[12] == \
        pytest.approx(810.693919, rel=1e-3)


def test_from_stat_missing_optical():
    """Test import from a stat file that is missing optical data"""
    stat_path = './tests/fixtures/stat/santamonica.stat'
    with pytest.raises(ValueError, match='Stat file contains no optical data.'):
        Wea.from_stat_file(stat_path)


def test_from_clear_sky():
    """Test from original clear sky"""
    location = Location(
        'Chicago Ohare Intl Ap', '-', 'USA', 41.98, -87.92, -6.0, 201.0)
    wea_from_clear_sky = Wea.from_ashrae_clear_sky(location)

    assert wea_from_clear_sky.location.city == 'Chicago Ohare Intl Ap'
    assert wea_from_clear_sky.timestep == 1
    assert wea_from_clear_sky.diffuse_horizontal_irradiance[0] == \
        pytest.approx(0, rel=1e-3)
    assert wea_from_clear_sky.direct_normal_irradiance[0] == \
        pytest.approx(0, rel=1e-3)
    assert wea_from_clear_sky.diffuse_horizontal_irradiance[12] == \
        pytest.approx(60.72258, rel=1e-3)
    assert wea_from_clear_sky.direct_normal_irradiance[12] == \
        pytest.approx(857.00439, rel=1e-3)


def test_from_zhang_huang():
    """Test from zhang huang solar model"""
    path = './tests/fixtures/epw/chicago.epw'
    epw = EPW(path)

    # test it first without pressure values
    wea_from_zh = Wea.from_zhang_huang_solar(
        epw.location, epw.total_sky_cover, epw.relative_humidity,
        epw.dry_bulb_temperature, epw.wind_speed)

    # include EPW pressure values
    wea_from_zh = Wea.from_zhang_huang_solar(
        epw.location, epw.total_sky_cover, epw.relative_humidity,
        epw.dry_bulb_temperature, epw.wind_speed, epw.atmospheric_station_pressure)

    assert wea_from_zh.location.city == 'Chicago Ohare Intl Ap'
    assert wea_from_zh.timestep == 1
    assert wea_from_zh.global_horizontal_irradiance[0] == \
        pytest.approx(0, rel=1e-1)
    assert wea_from_zh.global_horizontal_irradiance[12] == \
        pytest.approx(417.312, rel=1e-1)
    assert wea_from_zh.direct_normal_irradiance[12] == \
        pytest.approx(654.52, rel=1e-1)
    assert wea_from_zh.diffuse_horizontal_irradiance[12] == \
        pytest.approx(144.51, rel=1e-1)


def test_zhang_huang_accuracy():
    """Test zhang huang solar model to ensure that average error is within
    25% of actual solar."""
    path = './tests/fixtures/epw/chicago.epw'
    epw = EPW(path)

    wea = Wea.from_zhang_huang_solar(
        epw.location, epw.total_sky_cover, epw.relative_humidity,
        epw.dry_bulb_temperature, epw.wind_speed, epw.atmospheric_station_pressure)

    # test global horizontal radiation
    glob_horiz_error = [abs(i - j) for i, j in zip(
        epw.global_horizontal_radiation,
        wea.global_horizontal_irradiance)]
    avg_glob_horiz_error = sum(glob_horiz_error) / sum(
        epw.global_horizontal_radiation)
    assert (sum(glob_horiz_error) / 8760) < 50
    assert avg_glob_horiz_error < 0.5

    # test direct normal radiation
    dir_normal_error = [abs(i - j) for i, j in zip(
        epw.direct_normal_radiation, wea.direct_normal_irradiance)]
    avg_dir_normal_error = sum(dir_normal_error) / sum(
        epw.direct_normal_radiation)
    assert sum(dir_normal_error) / 8760 < 100
    assert avg_dir_normal_error < 0.5

    # test diffuse horizontal radiation
    dif_horiz_error = [abs(i - j) for i, j in zip(
        epw.diffuse_horizontal_radiation,
        wea.diffuse_horizontal_irradiance)]
    avg_dif_horiz_error = sum(dif_horiz_error) / sum(
        epw.diffuse_horizontal_radiation)
    assert sum(dif_horiz_error) / 8760 < 50
    assert avg_dif_horiz_error < 0.5


def test_equality():
    """Test the equality of files imported from the same source."""
    wea_file = './tests/fixtures/wea/chicago.wea'
    wea_1 = Wea.from_file(wea_file)
    wea_2 = Wea.from_file(wea_file)
    assert wea_1 == wea_2

    wea_2.direct_normal_irradiance[12] = 200
    assert wea_1 != wea_2


def test_dict_methods():
    """Test JSON serialization methods"""
    # test first with a continuous annual Wea
    epw_path = './tests/fixtures/epw/chicago.epw'
    wea = Wea.from_epw_file(epw_path)
    assert wea.to_dict() == Wea.from_dict(wea.to_dict()).to_dict()

    # then test with a filtered Wea including datetimes in the dict
    wea_file = './tests/fixtures/wea/chicago_filtered.wea'
    wea = Wea.from_file(wea_file)
    assert wea.to_dict() == Wea.from_dict(wea.to_dict()).to_dict()


def test_import_epw():
    """Test to compare import from epw with its dict version."""
    epw_path = './tests/fixtures/epw/chicago.epw'
    wea_from_epw = Wea.from_epw_file(epw_path)

    wea_dict = wea_from_epw.to_dict()
    wea_from_dict = Wea.from_dict(wea_dict)
    assert wea_from_dict.direct_normal_irradiance.values == \
        wea_from_epw.direct_normal_irradiance.values
    assert wea_from_dict.diffuse_horizontal_irradiance.values == \
        wea_from_epw.diffuse_horizontal_irradiance.values


def test_import_stat():
    """Test to compare import from stat with its dict version."""
    stat_path = './tests/fixtures/stat/chicago.stat'
    wea_from_stat = Wea.from_stat_file(stat_path)

    wea_dict = wea_from_stat.to_dict()
    wea_from_dict = Wea.from_dict(wea_dict)
    assert wea_from_dict.direct_normal_irradiance.values == \
        wea_from_stat.direct_normal_irradiance.values
    assert wea_from_dict.diffuse_horizontal_irradiance.values == \
        wea_from_stat.diffuse_horizontal_irradiance.values


def test_write_wea():
    """Test the write Wea file capability."""
    stat_path = './tests/fixtures/stat/chicago.stat'
    wea_from_stat = Wea.from_stat_file(stat_path)

    wea_path = './tests/fixtures/wea/chicago_stat.wea'
    hrs_path = './tests/fixtures/wea/chicago_stat.hrs'
    wea_from_stat.write(wea_path, True)

    assert os.path.isfile(wea_path)
    assert os.stat(wea_path).st_size > 1
    assert os.path.isfile(hrs_path)
    assert os.stat(hrs_path).st_size > 1

    # check the order of the data in the file
    with open(wea_path) as wea_f:
        lines = wea_f.readlines()
        assert float(lines[6].split(' ')[-2]) == \
            pytest.approx(
                wea_from_stat.direct_normal_irradiance[0], rel=1e-1)
        assert int(lines[6].split(' ')[-1]) == \
            wea_from_stat.diffuse_horizontal_irradiance[0]
        assert float(lines[17].split(' ')[-2]) == \
            pytest.approx(
                wea_from_stat.direct_normal_irradiance[11], rel=1e-1)
        assert float(lines[17].split(' ')[-1]) == \
            pytest.approx(
                wea_from_stat.diffuse_horizontal_irradiance[11], rel=1e-1)

    os.remove(wea_path)
    os.remove(hrs_path)


def test_global_and_direct_horizontal():
    """Test the global horizontal irradiance on method."""
    stat_path = './tests/fixtures/stat/chicago.stat'
    wea_from_stat = Wea.from_stat_file(stat_path)

    diffuse_horiz_rad = wea_from_stat.diffuse_horizontal_irradiance
    direct_horiz_rad = wea_from_stat.direct_horizontal_irradiance
    glob_horiz_rad = wea_from_stat.global_horizontal_irradiance

    assert [x for x in glob_horiz_rad] == pytest.approx(
        [x + y for x, y in zip(diffuse_horiz_rad, direct_horiz_rad)], rel=1e-3)


def test_directional_irradiance():
    """Test the directional irradiance method."""
    stat_path = './tests/fixtures/stat/chicago.stat'
    wea_from_stat = Wea.from_stat_file(stat_path)

    srf_total, srf_direct, srf_diffuse, srf_reflect = \
        wea_from_stat.directional_irradiance(90)
    diffuse_horiz_rad = wea_from_stat.diffuse_horizontal_irradiance
    direct_horiz_rad = wea_from_stat.direct_horizontal_irradiance
    glob_horiz_rad = wea_from_stat.global_horizontal_irradiance

    assert srf_total.values == pytest.approx(glob_horiz_rad.values, rel=1e-3)
    assert srf_direct.values == pytest.approx(direct_horiz_rad.values, rel=1e-3)
    assert srf_diffuse.values == pytest.approx(diffuse_horiz_rad.values, rel=1e-3)
    assert srf_reflect.values == pytest.approx([0] * 8760, rel=1e-3)


def test_estimate_illuminance():
    """Test the directional irradiance method."""
    epw_path = './tests/fixtures/epw/chicago.epw'
    epw = EPW(epw_path)
    wea = Wea.from_epw_file(epw_path)

    glob_ill, dir_ill, diff_ill, zen_lum = \
        wea.estimate_illuminance_components(epw.dew_point_temperature)

    assert glob_ill.bounds[0] == pytest.approx(0, rel=1e-3)
    assert 100000 < glob_ill.bounds[1] < 125000
    assert dir_ill.bounds[0] == pytest.approx(0, rel=1e-3)
    assert 75000 < dir_ill.bounds[1] < 125000
    assert diff_ill.bounds[0] == pytest.approx(0, rel=1e-3)
    assert 50000 < diff_ill.bounds[1] < 100000
    assert zen_lum.bounds[0] == pytest.approx(0, rel=1e-3)
    assert zen_lum.bounds[1] < 35000


def test_leap_year():
    """Test clear sky with leap year."""
    location = Location(
        'Chicago Ohare Intl Ap', '-', 'USA', 41.98, -87.92, -6.0, 201.0)
    wea = Wea.from_ashrae_clear_sky(location, is_leap_year=True)

    assert wea.diffuse_horizontal_irradiance.datetimes[1416].month == 2
    assert wea.diffuse_horizontal_irradiance.datetimes[1416].day == 29
    assert wea.diffuse_horizontal_irradiance.datetimes[1416].hour == 0

    assert wea.diffuse_horizontal_irradiance.datetimes[1416 + 12].month == 2
    assert wea.diffuse_horizontal_irradiance.datetimes[1416 + 12].day == 29
    assert wea.diffuse_horizontal_irradiance.datetimes[1416 + 12].hour == 12


def test_filter_by_pattern():
    """Test the filter_by_pattern method"""
    epw_path = './tests/fixtures/epw/chicago.epw'
    wea_from_epw = Wea.from_epw_file(epw_path)

    pattern = [False] * 8 + [True] * 8 + [False] * 8
    filtered_wea = wea_from_epw.filter_by_pattern(pattern)
    assert len(filtered_wea) == int(8760 / 3)


def test_filter_by_hoys_and_moys():
    """Test the filter_by_hoys and the filter_by_moys method"""
    epw_path = './tests/fixtures/epw/chicago.epw'
    wea_from_epw = Wea.from_epw_file(epw_path)

    hoys = list(range(24))
    filtered_wea = wea_from_epw.filter_by_hoys(hoys)
    assert len(filtered_wea) == len(hoys)

    moys = list(range(0, 24 * 60, 60))
    filtered_wea = wea_from_epw.filter_by_moys(moys)
    assert len(filtered_wea) == len(moys)


def test_filter_by_analysis_period():
    """Test the filter_by_analysis_period method"""
    epw_path = './tests/fixtures/epw/chicago.epw'
    wea_from_epw = Wea.from_epw_file(epw_path)

    a_period = AnalysisPeriod(12, 21, 0, 3, 21, 23)
    filtered_wea = wea_from_epw.filter_by_analysis_period(a_period)
    assert len(filtered_wea) == len(filtered_wea.diffuse_horizontal_irradiance.values) \
        == len(a_period)
    assert not filtered_wea.is_annual
    assert filtered_wea.is_continuous

    wea_path = './tests/fixtures/wea/chicago_winter.wea'
    filtered_wea.write(wea_path)
    assert os.path.isfile(wea_path)
    assert os.stat(wea_path).st_size > 1
    os.remove(wea_path)


def test_filter_by_sun_up():
    """Test the filter_by_sun_up method"""
    epw_path = './tests/fixtures/epw/chicago.epw'
    wea_from_epw = Wea.from_epw_file(epw_path)

    wea = wea_from_epw.filter_by_sun_up()
    assert isinstance(wea.direct_normal_irradiance, HourlyDiscontinuousCollection)
    assert isinstance(wea.diffuse_horizontal_irradiance, HourlyDiscontinuousCollection)
    assert not wea.is_annual
    assert not wea.is_continuous
    assert len(wea) == 4427
    assert wea.datetimes[0].hour == 7
