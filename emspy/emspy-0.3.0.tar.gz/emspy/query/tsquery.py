from __future__ import print_function
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from emspy.query import *
from .query import Query

import sys
import pickle
import warnings
import pandas as pd
import numpy as np


class TSeriesQuery(Query):


    def __init__(self, conn, ems_name, data_file = LocalData.default_data_file):

        Query.__init__(self, conn, ems_name)
        self._init_assets(data_file)
        self.reset()


    def _init_assets(self, data_file):

        # Query._init_assets(self)
        self.__analytic = Analytic(self._conn, self._ems_id, data_file)


    def reset(self):

        self.__columns  = list()
        self.__queryset = {'select':[]}


    def select_ids(self, analytic_ids, names=None, descriptions=None, units=None, lookup=False):
        """
        A method for selecting parameters to query for by analytic_id.  This method adds analytics and relevant
        information as provided.  It can also query the EMS API for relevant information if requested.

        Args:
            analytic_ids (:obj:`list` of :obj:`str`): A list of analytic_ids to select and query for.
            names (:obj:`list` of :obj:`str`): A list of names for each analytic_id in analytic_ids.

            descriptions (:obj:`list` of :obj:`str`, optional): A list of descriptions for each analytic_id in
                analytic_ids.
            units (:obj:`list` of :obj:`str`, optional): A list of units for each analytic_id in analytic_ids.
            names (:obj:`list` of :obj:`str`, optional): A list of names for each analytic_id in analytic_ids.
            lookup (:obj:`bool`, optional): Whether or not to look up names, descriptions and units using the EMS API.
        Raises:
            ValueError: If `analytic_ids`, `names`, `descriptions` (if specified), and `units` (if specified) are not
                of the same length.
            ValueError: If `analytic_ids`, and `names` are not both defined, unless `lookup=True` is specified, in which
                case names can be None.
            TypeError: If `analytic_ids` is a string, but `names`, `descriptions`, and `units` are specified as
                something other than strings.
        """

        # We require names if we are not going to look up metadata about the analytic_ids.
        # We could just allow adding analytic_ids, but the user will likely have to pair the results up with names
        # information anyway, so it might as well be provided to the select_ids method for a more friendly experience.
        if names is None and not lookup:
            raise ValueError("If `names` is not specified, you must set `lookup`=True")

        # If the input parameters are both strings, then we will cast them into lists so we can proceed as normal
        # (i.e. loop through them [once])
        if isinstance(analytic_ids, str):
            analytic_ids = [analytic_ids]
            # if names is not None, and names is not a string type object, raise an error.
            if names is not None:
                if isinstance(names, str):
                    names = [names]
                else:
                    raise TypeError("If a string is passed for `analytic_ids`, `names` must be a string as well.")

            # if descriptions is not None, and descriptions is not a string type object, raise an error.
            if descriptions is not None:
                if isinstance(descriptions, str):
                    descriptions = [descriptions]
                else:
                    raise ValueError("If a string is passed for `analytic_ids`, `descriptions` must be a string as "
                                     "well.")

            # if units is not None, and units is not a string type object, raise an error.
            if units is not None:
                if isinstance(units, str):
                    units = [units]
                else:
                    raise ValueError("If a string is passed for `analytic_ids`, `units` must be a string as well.")

        # calculate the length of each input list
        # descriptions and units aren't necessarily input lists (could be None), but they are necessarily the same
        # length as analytic_ids
        lengths = {'analytic_ids': len(analytic_ids)}
        if names is not None:
            lengths['names'] = len(names)
        if descriptions is not None:
            lengths['descriptions'] = len(descriptions)
        if units is not None:
            lengths['units'] = len(units)

        length_set = set(lengths.values())  # This is a set of unique lengths

        # If there is more than one unique iterable length, then one must be wrong.  Return an error.
        if len(length_set) > 1:
            error_str = ''
            for list_name, list_length in lengths.items():
                error_str = error_str + '\t\t{0:15}: {1}\n'.format(list_name, str(list_length))
            raise ValueError("All lists must be of the same length.  Found lengths:\n{0}".format(error_str))

        # Fill out lists with empty strings that are the same length as the analytic_ids list, if parameters are None.
        names = ['']*len(analytic_ids) if names is None else names
        descriptions = ['']*len(analytic_ids) if descriptions is None else descriptions
        units = ['']*len(analytic_ids) if units is None else units

        # loop over items
        for analytic_id, name, description, unit in zip(analytic_ids, names, descriptions, units):
            # if we aren't performing a lookup, just stuff in the lists that have been passed in.
            if not lookup:
                prm = {'id': analytic_id, 'name': name, 'description': description, 'units': unit,
                       'ems_id': self._ems_id}
            # if we are performing a lookup, we need to make an API call to get relevant data.
            else:
                prm = self.__analytic.get_param_details(analytic_id)
                prm['ems_id'] = self._ems_id
            df = pd.DataFrame(prm, index=[0])

            self.__analytic._param_table = self.__analytic._param_table.append(df, ignore_index=True, sort=True)

            # Put the param into JSON query string
            self.__queryset['select'].append({'analyticId': prm['id']})
            # Just in case you want to check what params are selected
            self.__columns.append(prm)

            self.__analytic._save_paramtable()


    def select(self, *args):
        """
        A method for selecting parameters to query for by name.  This method searches for parameters by name and adds
        them to the current query.  If multiple matches for a given parameter are found, the match with the shortest
        name is selected.

        Args:
            *args (:obj:`list` of :obj:`str`): Variable length argument list of parameter names.
        """

        keywords   = args
        save_table = False

        for kw in keywords:
            # Get the param from param table
            prm = self.__analytic.get_param(kw)
            if prm['id'] == "":
                # If the param's not found, call EMS API
                res_df = self.__analytic.search_param(kw, in_df = True)
                res_df['ems_id'] = self._ems_id
                # The first one is with the shortest name string. Pick that.
                prm = res_df.iloc[0,:].to_dict()
                # Add the new parameters to the param table for later uses
                self.__analytic._param_table = self.__analytic._param_table.append(res_df, ignore_index = True, sort = True)
                save_table = True

            # Put the param into JSON query string
            self.__queryset['select'].append({'analyticId': prm['id']})
            # Just in case you want to check what params are selected
            self.__columns.append(prm)
        if save_table:
            self.__analytic._save_paramtable()


    def range(self, start = None, end = None):

        self.__queryset['start'] = start
        self.__queryset['end']   = end


    def timepoint(self, tpoint):
        if type(tpoint) == np.ndarray:
            tpoint = tpoint.tolist()
        self.__queryset['offsets'] = tpoint


    def run(self, flight, start = None, end = None, timestep = None, timepoint = None,
            discretes_as_strings=True):

        # if start is None:
        #     start = 0.0

        # if end is None:
        #     end = self.flight_duration(flight)

        # if timestep is not None:
        #     timepoint = np.arange(start, end, timestep)

        # if timepoint is not None:
        #     self.timepoint(timepoint)
        # else:
        #     self.range(start, end)
        if timepoint is not None:
            self.timepoint(timepoint)

        # allow the user to specify discretesAsStrings = 'false'
        # per the EMS API documentation, discretesAsStrings is true by default.  So it will only get set to false if
        # that option is specified.  This will allow users to return discretes in time series parameters as int values.
        if not discretes_as_strings:
            self.__queryset['discretesAsStrings'] = 'false'

        elif timestep is not None:
            start = 0.0 if start is None else start

            if end is None:
                raise ValueError("End timepoint should be given along with timestep input.")

            self.timepoint(np.arange(start, end+1e-10, timestep))

        else:
            self.range(start, end)

        resp_h, content = self._conn.request( uri_keys = ("analytic", "query"),
                                              uri_args = (self._ems_id, flight),
                                              jsondata = self.__queryset)

        if 'message' in content:
            sys.exit('API query for flight %d was unsuccessful.\nHere is the message from API: %s' % (flight, content['message']))
        
        # Put the data in Pandas DataFrame
        df = pd.DataFrame({"Time (sec)": content['offsets']})

        for i, prm in enumerate(self.__columns):
            df[prm['name']] = content['results'][i]['values']

        ## "\r\x1b[K" is overwrite print.
        return df



    def multi_run(self, flight, start = None, end = None, timestep=None, timepoint = None, save_file = None, verbose = True):

        res       = list()
        attr_flag = False
        if isinstance(flight, pd.DataFrame):
            FR = flight["Flight Record"]
            attr_flag = True
        else:
            FR = flight

        # param processing
        if start is None:       start       = [None]*len(FR)
        if end   is None:       end         = [None]*len(FR)
        if not hasattr(timestep, "__len__"):
            timestep = [timestep]*len(FR)
        if timepoint is None:   
            timepoint   = [None]*len(FR)
        else: 
            warnings.warn("Time points are not yet supported. The given time points will be ignored.")
            timepoint   = [None]*len(FR)
            
        if verbose: print('\n=== Start running time-series data querying for %d flights ===\n' % len(FR))
        
        for i, fr in enumerate(FR):
            if verbose: print('\r\x1b[K%d / %d: FR %d' % (i+1, len(FR), fr), end=' ')
            i_res = dict()
            if attr_flag:
                i_res['flt_data'] = flight.iloc[i,:].to_dict()
            else:
                i_res['flt_data'] = {'Flight Record': fr}
            i_res['ts_data'] = self.run(fr, start[i], end[i], timestep[i])
            res.append(i_res)

            if save_file is not None:
                pickle.dump(res, open(save_file, 'wb'))
        if verbose: print('Done')

        return res


    def flight_duration(self, flight, unit = "second"):
        '''
        deprecated
        '''

        p = self.__analytic.get_param("hours of data (hours)")
        if p["id"] == "":
            res_df = self.__analytic.search_param("hours of data (hours)", in_df = True)
            p      = res_df.iloc[0].to_dict()
            self.__analytic._param_table = self.__analytic._param_table.append(res_df, ignore_index = True, sort = True)
            self.__analytic._save_paramtable()
        q = {
            "select": [{"analyticId": p["id"]}],
            "size": 1
        }

        resp_h, content = self._conn.request( uri_keys = ("analytic", "query"),
                                              uri_args = (self._ems_id, flight),
                                              jsondata = q)
        if 'message' in content:
            sys.exit('API query for flight %d, parameter = "%s" was unsuccessful.\nHere is the message from API: %s' % (flight, p['name'], content['message']))
        fl_len = content['results'][0]['values'][0]

        if unit == "second":
            t = fl_len * 60 * 60
        elif unit == "minute":
            t = fl_len * 60
        elif unit == "hour":
            t = fl_len
        else:
            sys.exit("Unrecognizable time unit (%s)." % unit)
        return t

    def get_queryset(self):
        """
        Returns a dictionary with the queryset for the current time series query.

        Returns:
            list: a list describing the current queryset.
        """

        return self.__queryset

