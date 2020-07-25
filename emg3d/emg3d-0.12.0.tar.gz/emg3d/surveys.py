"""

:mod:`survey` -- Surveys
========================

A survey stores a set of sources, receivers, and the measured data.

"""
# Copyright 2018-2020 The emg3d Developers.
#
# This file is part of emg3d.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy
# of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations under
# the License.

from copy import deepcopy
from dataclasses import dataclass

import numpy as np

try:
    import xarray
except ImportError:
    xarray = None

from emg3d import utils

__all__ = ['Survey', 'Dipole', 'PointDipole']


class Survey:
    """Create a survey with sources, receivers, and data.

    A survey contains all the sources with their frequencies, receivers, and
    corresponding data.

    Underlying the survey-class is an xarray, which is basically a regular
    ndarray with axis labels and more. The module `xarray` is a soft
    dependency, and has to be installed manually to use the `Survey`
    functionality.

    This class was developed with a node-based, marine CSEM survey layout in
    mind. It is therefore optimised for and mostly tested with that setup. This
    means for a number of receivers which measure for all source positions. The
    general layout of the data for such a survey is (S, R, F), where `S` is the
    number of sources, `R` the number of receivers, and `F` the number of
    frequencies::

                             f1
            Rx1 Rx2  .  RxR /   f2
           ┌───┬───┬───┬───┐   /   .
       Tx1 │   │   │   │   │──┐   /   fF
           ├───┼───┼───┼───┤  │──┐   /
       Tx2 │   │   │   │   │──┤  │──┐
           ├───┼───┼───┼───┤  │──┤  │
        .  │   │   │   │   │──┤  │──┤
           ├───┼───┼───┼───┤  │──┤  │
       TxS │   │   │   │   │──┤  │──┤
           └───┴───┴───┴───┘  │──┤  │
              └───┴───┴───┴───┘  │──┤
                 └───┴───┴───┴───┘  │
                    └───┴───┴───┴───┘

    However, the class can also be used for a CSEM streamer-style survey
    layout (by setting `fixed=True`), where there is a moving source with one
    or several receivers at a fixed offset. The layout of the data is then also
    (S, R, F), but here `S` is the number of locations of the only source, `R`
    is the number of receiver-offsets, and `F` is the number of frequencies::

                                        f1
                Offs1     .   OffsR    /   .
              ┌─────────┬───┬─────────┐   /   fF
       TxPos1 │ Rx1-TP1 │ . │ RxR-TP1 │──┐   /
              ├─────────┼───┼─────────┤  │──┐
       TxPos2 │ Rx1-TP2 │ . │ RxR-TP2 │──┤  │
              ├─────────┼───┼─────────┤  │──┤
        .     │ .       │ . │ .       │──┤  │
              ├─────────┼───┼─────────┤  │──┤
       TxPosS │ Rx1-TPS │ . │ RxR-TPS │──┤  │
              └─────────┴───┴─────────┘  │──┤
                 └─────────┴───┴─────────┘  │
                    └─────────┴───┴─────────┘

    This means that even though there is only one source, there are actually
    `S` source dipoles, as each position is treated as a different dipole. The
    number of receiver dipoles in this case is `SxR`. This setup can also be
    used for airborne EM.


    Parameters
    ----------
    name : str
        Name of the survey

    sources, receivers : tuple, list, or dict
        Sources and receivers.

        - Tuples: Coordinates in one of the two following formats:

          - `(x, y, z, azimuth, dip)` [m, m, m, °, °];
          - `(x0, x1, y0, y1, z0, z1)` [m, m, m, m, m, m].

          Dimensions will be expanded (hence, if `n` dipoles, each parameter
          must have length 1 or `n`). These dipoles will be named sequential
          with `Tx###` and `Rx###`.

          The tuple can additionally contain an additional element at the end
          (after `dip` or `z1`), `electric`, a boolean of length 1 or `n`, that
          indicates if the dipoles are electric or magnetic.

        - List: A list of :class:`Dipole`-instances. The names of all dipoles
          in the list must be unique.

        - Dictionary: A dict of de-serialized :class:`Dipole`-instances; mainly
          used for loading from file.

    frequencies : ndarray
        Source frequencies (Hz).

    data : ndarray or None
        The observed data (dtype=np.complex128); must have shape (nsrc, nrec,
        nfreq) or, if `fixed=True`, (nsrc, noff, nfreq). If None, it will be
        initiated with NaN's.

    fixed : bool
        Node-based CSEM survey (`fixed=False`; default) or streamer-type CSEM
        survey (`fixed=True`). In the streamer-type survey, the number of
        `receivers` supplied must be a multiple of the source positions.
        In this case, the receivers are grouped into offsets.


    """
    # Currently, `surveys.data` contains an :class:`xarray.Dataset`. As such,
    # the `Survey`-Class has an xarray-dataset as one of its attributes.
    # Probably there would be a cleaner way to simply use xarray instead of a
    # dedicated `Survey`-Class by utilizing, e.g.,
    # :func:`xarray.register_dataset_accessor`.

    def __init__(self, name, sources, receivers, frequencies, data=None,
                 fixed=0):
        """Initiate a new Survey instance."""

        # Store survey name and fixed.
        self.name = name
        self.fixed = fixed

        # Initiate sources.
        self._sources = self._dipole_info_to_dict(sources, 'source')

        # Initiate receivers.
        self._receivers = self._dipole_info_to_dict(receivers, 'receiver')

        # Initiate frequencies.
        self._frequencies = np.array(frequencies, dtype=np.float64, ndmin=1)

        # Initialize xarray dataset.
        self._initiate_dataset(data)

    @utils._requires('xarray')
    def _initiate_dataset(self, data):
        """Initiate Dataset; wrapped in fct to check if xarray is installed."""

        # Initialize NaN-data if not provided.
        if data is None:
            data = np.ones((len(self._sources), len(self._receivers),
                            self._frequencies.size),
                           dtype=np.complex128)*np.nan
        else:
            data = np.atleast_3d(data)

        # Create Dataset.
        self._data = xarray.Dataset(
            {'observed': xarray.DataArray(data, dims=('src', 'rec', 'freq'))},
            coords={'src': list(self.sources.keys()),
                    'rec': list(self.receivers.keys()),
                    'freq': list(self.frequencies)},
        )

        # Add attributes.
        self._data.src.attrs['long_name'] = 'Source dipole'
        self._data.src.attrs['src-dipoles'] = self.sources
        self._data.rec.attrs['long_name'] = 'Receiver dipole'
        self._data.rec.attrs['rec-dipoles'] = self.receivers
        self._data.freq.attrs['long_name'] = 'Source frequency'
        self._data.freq.attrs['units'] = 'Hz'

    def __repr__(self):
        return (f"{self.__class__.__name__}: {self.name}\n\n"
                f"{self.data.__repr__()}")

    def _repr_html_(self):
        return (f"<h4>{self.__class__.__name__}: {self.name}</h4><br>"
                f"{self.data._repr_html_()}")

    def copy(self):
        """Return a copy of the Survey."""
        return self.from_dict(self.to_dict(True))

    def to_dict(self, copy=False):
        """Store the necessary information of the Survey in a dict."""

        out = {'name': self.name, '__class__': self.__class__.__name__}

        # Add sources.
        out['sources'] = {k: v.to_dict() for k, v in self.sources.items()}

        # Add receivers.
        if self.fixed:
            rec = {}
            for key, value in self.receivers.items():
                rec[key] = {k: v.to_dict() for k, v in value.items()}
        else:
            rec = {k: v.to_dict() for k, v in self.receivers.items()}
        out['receivers'] = rec

        # Add frequencies.
        out['frequencies'] = self.frequencies

        # Add data.
        out['observed'] = self.data.observed.values

        # Fixed.
        out['fixed'] = int(self.fixed)

        if copy:
            return deepcopy(out)
        else:
            return out

    @classmethod
    @utils._requires('xarray')
    def from_dict(cls, inp):
        """Convert dictionary into :class:`Survey` instance.

        Parameters
        ----------
        inp : dict
            Dictionary as obtained from :func:`Survey.to_dict`.
            The dictionary needs the keys `name`, `sources`, `receivers`
            `frequencies`, `observed`, and `fixed`.

        Returns
        -------
        obj : :class:`Survey` instance

        """
        try:
            return cls(name=inp['name'], sources=inp['sources'],
                       receivers=inp['receivers'],
                       frequencies=inp['frequencies'], data=inp['observed'],
                       fixed=bool(inp['fixed']))

        except KeyError as e:
            raise KeyError(f"Variable {e} missing in `inp`.") from e

    def to_file(self, fname, compression="gzip", json_indent=2, verb=1):
        """Store Survey to a file.

        Parameters
        ----------
        fname : str
            File name inclusive ending, which defines the used data format.
            Implemented are currently:

            - `.h5` (default): Uses `h5py` to store inputs to a hierarchical,
              compressed binary hdf5 file. Recommended file format, but
              requires the module `h5py`. Default format if ending is not
              provided or not recognized.
            - `.npz`: Uses `numpy` to store inputs to a flat, compressed binary
              file. Default format if `h5py` is not installed.
            - `.json`: Uses `json` to store inputs to a hierarchical, plain
              text file.

        compression : int or str, optional
            Passed through to h5py, default is 'gzip'.

        json_indent : int or None
            Passed through to json, default is 2.

        verb : int
            Silent if 0, verbose if 1.
        """
        from emg3d import io
        io.save(fname, compression=compression, json_indent=json_indent,
                collect_classes=False, verb=verb, survey=self)

    @classmethod
    @utils._requires('xarray')
    def from_file(cls, fname, verb=1):
        """Load Survey from a file.

        Parameters
        ----------
        fname : str
            File name including extension. Used backend depends on the file
            extensions:

            - '.npz': numpy-binary
            - '.h5': h5py-binary (needs `h5py`)
            - '.json': json

        verb : int
            Silent if 0, verbose if 1.

        Returns
        -------
        survey : :class:`Survey`
            The survey that was stored in the file.

        """
        from emg3d import io
        return io.load(fname, verb=verb)['survey']

    @property
    def shape(self):
        """Return nsrc x nrec x nfreq.

        Note that not all source-receiver-frequency pairs do actually have
        data. Check `size` to see how many data points there are.
        """
        return self.data.observed.shape

    @property
    def size(self):
        """Return actual data size (does NOT equal nsrc x nrec x nfreq)."""
        return int(self.data.observed.count())

    @property
    def data(self):
        """Data, a :class:`xarray.DataSet` instance.

        Contains the :class:`xarray.DataArray` element `.observed`, but other
        data can be added. E.g., :class:`emg3d.simulations.Simulation` adds the
        `synthetic` array.
        """
        return self._data

    @property
    def sources(self):
        """Source dict containing all source dipoles."""
        return self._sources

    @property
    def receivers(self):
        """Receiver dict containing all receiver dipoles."""
        return self._receivers

    @property
    def src_coords(self):
        """Return source coordinates.

        The returned format is `(x, y, z, azm, dip)`, a tuple of 5 tuples.
        """

        return tuple(np.array([[s.xco, s.yco, s.zco, s.azm, s.dip] for s
                     in self.sources.values()]).T)

    @property
    def rec_coords(self):
        """Return receiver coordinates.

        The returned format is `(x, y, z, azm, dip)`, a tuple of 5 tuples. If
        `fixed=True` it returns a dict with the offsets as keys, and for each
        offset it returns the corresponding receiver coordinates as just
        outlined.
        """

        # Get receiver coordinates depending if fixed or not.
        if self.fixed:
            coords = {}
            for src in self.sources.keys():
                coords[src] = tuple(
                        np.array([[self.receivers[off][src].xco,
                                   self.receivers[off][src].yco,
                                   self.receivers[off][src].zco,
                                   self.receivers[off][src].azm,
                                   self.receivers[off][src].dip]
                                  for off in self.receivers.keys()]).T)
        else:
            coords = tuple(np.array([[r.xco, r.yco, r.zco, r.azm, r.dip] for r
                                     in self.receivers.values()]).T)

        return coords

    @property
    def frequencies(self):
        """Frequency array."""
        return self._frequencies

    def _dipole_info_to_dict(self, inp, name):
        """Create dict with provided source/receiver information."""

        # Create dict depending if `inp` is list, tuple, or dict.
        if isinstance(inp, list):  # List of Dipoles

            if self.fixed and name == 'receiver':  # Streamer-type receivers.

                # Get dimensions.
                nd = len(inp)
                ns = len(self.sources)  # Number of source position.
                nr = nd//ns             # Number of receivers / source.
                dnr = len(str(nr-1))    # Max number of digits; rec.

                # Create name lists.
                rec_names = [f"{i:0{dnr}d}" for i in range(nr)]
                src_names = list(self.sources.keys())

                # Ensure receivers are multiples of source positions.
                if nd % ns != 0:
                    raise ValueError(
                            "For fixed surveys, the number of receivers\n"
                            "must be a multiple of number of sources.\n"
                            f"Provided: #src: {ns}; #rec: {nd}.")

                # Assemble dict.
                out = {'Off'+name: {} for name in rec_names}
                for i, key in enumerate(out.keys()):
                    for ii, src_name in enumerate(src_names):
                        out[key][src_name] = inp[ii + i*ns]

            else:

                out = {d.name: d for d in inp}

                # Ensure that all names were unique:
                if len(out) != len(inp):
                    raise ValueError(
                            f"There are duplicate {name} names.\n"
                            f"Provided {name}s: {len(inp)}; "
                            f"unique names: {len(out)}.")

        elif isinstance(inp, tuple):  # Tuple with coordinates

            # See if last tuple element is boolean, hence el/mag-flag.
            if isinstance(inp[-1], (list, tuple, np.ndarray)):
                provided_elmag = isinstance(inp[-1][0], bool)
            else:
                provided_elmag = isinstance(inp[-1], bool)

            # Get max dimension.
            nd = max([np.array(n, ndmin=1).size for n in inp])

            # Expand coordinates.
            coo = np.array([nd*[val, ] if np.array(val).size == 1 else
                           val for val in inp], dtype=np.float64)

            # Extract el/mag flag or set to ones (electric) if not provided.
            if provided_elmag:
                elmag = coo[-1, :]
                coo = coo[:-1, :]
            else:
                elmag = np.ones(nd)

            # Create dipole names (number-strings).
            prefix = 'Tx' if name == 'source' else 'Rx'
            dnd = len(str(nd-1))  # Max number of digits.
            names = [f"{prefix}{i:0{dnd}d}" for i in range(nd)]

            # Create Dipole-dict.
            if self.fixed and name == 'receiver':  # Streamer-type receivers.

                # Get dimensions.
                ns = len(self.sources)  # Number of source position.
                nr = nd//ns             # Number of receivers / source.
                dnr = len(str(nr-1))    # Max number of digits; rec.

                # Create name lists.
                rec_names = [f"{i:0{dnr}d}" for i in range(nr)]
                src_names = list(self.sources.keys())

                # Ensure receivers are multiples of source positions.
                if nd % ns != 0:
                    raise ValueError(
                            "For fixed surveys, the number of receivers\n"
                            "must be a multiple of number of sources.\n"
                            f"Provided: #src: {ns}; #rec: {nd}.")

                # Assemble dict.
                out = {'Off'+rec_name: {} for rec_name in rec_names}
                for i, key in enumerate(out.keys()):
                    for ii, src_name in enumerate(src_names):
                        iii = ii + i*ns
                        out[key][src_name] = Dipole(
                                names[iii], coo[:, iii], elmag[iii])

            else:  # Default node-type src-rec comb. and src for streamer-type.
                out = {names[i]: Dipole(names[i], coo[:, i], elmag[i])
                       for i in range(nd)}

        elif isinstance(inp, dict):  # Dict of de-serialized Dipoles.
            if self.fixed and name == 'receiver':
                out = {}
                for k, v in inp.items():
                    out[k] = {k2: Dipole.from_dict(v2) for k2, v2 in v.items()}
            else:
                out = {k: Dipole.from_dict(v) for k, v in inp.items()}

        else:
            raise TypeError(
                    f"Input format of <{name}s> not recognized: {type(inp)}.")

        return out


# # Sources and Receivers # #
@dataclass(order=True, unsafe_hash=True)
class PointDipole:
    """Infinitesimal small electric or magnetic point dipole.

    Defined by its coordinates (xco, yco, zco), its azimuth (azm), its dip, and
    its type (electric).

    Not meant to be used directly. Use :class:`Dipole` instead.


    Parameters
    ----------
    name : str
        Dipole name.

    xco, yco, zco : float
        x-, y-, and z-coordinates (m).

    azm, dip : float
        Angles (in degrees °); coordinate system is right-handed with positive
        z up; East-North-Depth:

        - azimuth (°): horizontal deviation from x-axis, anti-clockwise.
        - +/-dip (°): vertical deviation from xy-plane down/up-wards.

    electric : bool
        Electric dipole if True, magnetic dipole otherwise. Default is True.

    """
    __slots__ = ['name', 'xco', 'yco', 'zco', 'azm', 'dip', 'electric']
    name: str
    xco: float
    yco: float
    zco: float
    azm: float
    dip: float
    electric: bool


class Dipole(PointDipole):
    """Finite length dipole or point dipole.

    Expansion of the basic :class:`PointDipole` to allow for finite length
    dipoles, and to provide coordinate inputs in the form of
    (x, y, z, azimuth, dip) or (x0, x1, y0, y1, z0, z1).

    Adds attributes `is_finite`, `electrode1`, `electrode2`, `length`, and
    `coordinates` to the class.

    For *point dipoles*, this gives it a length of unity (1 m), takes its
    coordinates as center, and computes the two electrode positions.

    For *finite length dipoles* it sets the coordinates to its center and
    computes its length, azimuth, and dip.

    Finite length dipoles and point dipoles have therefore the exactly same
    signature, and can only be distinguished by the attribute `is_finite`.


    Parameters
    ----------
    name : str
        Dipole name.

    coordinates : tuple of floats
        Source coordinates, one of the following:

        - (x0, x1, y0, y1, z0, z1): finite length dipole,
        - (x, y, z, azimuth, dip): point dipole.

        The coordinates x, y, and z are in meters (m), the azimuth and dip in
        degree (°).

        Angles (coordinate system is right-handed with positive z up;
        East-North-Depth):

        - azimuth (°): horizontal deviation from x-axis, anti-clockwise.
        - +/-dip (°): vertical deviation from xy-plane down/up-wards.

    electric : bool
        Electric dipole if True, magnetic dipole otherwise. Default is True.

    """
    # These are the only kwargs that do not raise a warning.
    # These are also the only ones which are (de-)serialized.
    accepted_keys = ['strength', ]

    def __init__(self, name, coordinates, electric=True, **kwargs):
        """Check coordinates and kwargs."""

        # Add additional info to the dipole.
        for key, value in kwargs.items():
            if key not in self.accepted_keys:
                print(f"* WARNING :: Unknown kwargs {{{key}: {value}}}")
            setattr(self, key, value)

        # Conversion to float-array fails if there are lists and tuples within
        # the tuple, or similar. This should also catch many wrong inputs.
        coords = np.array(coordinates, dtype=np.float64)

        # Check size => finite or point dipole?
        if coords.size == 5:
            self.is_finite = False

        elif coords.size == 6:
            self.is_finite = True

            # Ensure the two poles are distinct.
            if np.allclose(coords[::2], coords[1::2]):
                raise ValueError(
                        "The two poles are identical, use the format\n"
                        "(x, y, z, azimuth, dip) instead.\n"
                        f"Provided coordinates: {coordinates}.")

        else:
            raise ValueError(
                    "Dipole coordinates are wrong defined. They must be\n"
                    "defined either as a point, (x, y, z, azimuth, dip), or\n"
                    "as two poles, (x0, x1, y0, y1, z0, z1), all floats.\n"
                    f"Provided coordinates: {coordinates}.")

        # Angles: Very small angles are set to zero, because, e.g.,
        #         cos(pi/2) is roughly 6.12e-17, not 0.

        # Get xco, yco, zco, azm, and dip.
        if self.is_finite:

            # Get the two separate electrodes.
            self.electrode1 = tuple(coords[::2])
            self.electrode2 = tuple(coords[1::2])

            # Compute center.
            xco, yco, zco = np.sum(coords.reshape(3, -1), 1)/2

            # Get lengths in each direction.
            dx, dy, dz = np.diff(coords.reshape(3, -1)).ravel()

            # Length of bipole.
            self.length = np.linalg.norm([dx, dy, dz], axis=0)

            # Horizontal deviation from x-axis.
            azm = np.round(np.rad2deg(np.arctan2(dy, dx)), 5)

            # Vertical deviation from xy-plane down.
            dip = np.round(np.rad2deg(np.pi/2-np.arccos(dz/self.length)), 5)

        else:
            # Get coordinates, angles, and set length.
            xco, yco, zco, azm, dip = tuple(coords)
            self.length = 1.0

            # Get lengths in each direction (total length is 1).
            dx = np.round(np.cos(np.deg2rad(azm))*np.cos(np.deg2rad(dip)), 5)
            dy = np.round(np.sin(np.deg2rad(azm))*np.cos(np.deg2rad(dip)), 5)
            dz = np.round(np.sin(np.deg2rad(dip)), 5)

            # Get the two separate electrodes.
            self.electrode1 = (xco-dx/2, yco-dy/2, zco-dz/2)
            self.electrode2 = (xco+dx/2, yco+dy/2, zco+dz/2)

        super().__init__(name, xco, yco, zco, azm, dip, bool(electric))

    def __repr__(self):
        return (f"{self.__class__.__name__}({self.name}, "
                f"{['H', 'E'][self.electric]}, "
                f"{{{self.xco:,.1f}m; {self.yco:,.1f}m; {self.zco:,.1f}m}}, "
                f"θ={self.azm:.1f}°, φ={self.dip:.1f}°, "
                f"l={self.length:,.1f}m)")

    @property
    def coordinates(self):
        """Return coordinates.

        Returns
        -------
        coords : tuple
            Coordinates in the format (x, y, z, azimuth, dip) or (x0, x1, y0,
            y1, z0, z1). This format is used in many other routines.
        """
        if self.is_finite:
            return (self.electrode1[0], self.electrode2[0],
                    self.electrode1[1], self.electrode2[1],
                    self.electrode1[2], self.electrode2[2])
        else:
            return (self.xco, self.yco, self.zco, self.azm, self.dip)

    def copy(self):
        """Return a copy of the Dipole."""
        return self.from_dict(self.to_dict(True))

    def to_dict(self, copy=False):
        """Store the necessary information of the Dipole in a dict."""
        out = {'name': self.name, 'coordinates': self.coordinates,
               'electric': self.electric, '__class__': self.__class__.__name__}

        # Add accepted kwargs.
        for key in self.accepted_keys:
            if hasattr(self, key):
                out[key] = getattr(self, key)

        if copy:
            return deepcopy(out)
        else:
            return out

    @classmethod
    def from_dict(cls, inp):
        """Convert dictionary into :class:`Dipole` instance.

        Parameters
        ----------
        inp : dict
            Dictionary as obtained from :func:`Dipole.to_dict`. The dictionary
            needs the keys `name`, `coordinates`, and `electric`.

        Returns
        -------
        obj : :class:`Dipole` instance

        """
        try:
            kwargs = {k: v for k, v in inp.items() if k in cls.accepted_keys}
            return cls(name=inp['name'], coordinates=inp['coordinates'],
                       electric=inp['electric'], **kwargs)
        except KeyError as e:
            raise KeyError(f"Variable {e} missing in `inp`.") from e
