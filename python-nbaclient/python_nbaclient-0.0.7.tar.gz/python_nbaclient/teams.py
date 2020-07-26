from python_nbaclient import REQ_HEADER
from python_nbaclient.constants import EndPoints, StatusCode
from python_nbaclient.constants import CURRENT_SEASON, LEAGUE_ID, TEAM_TO_ID, ID_TO_TEAM
from python_nbaclient.utils import Query, Output

endpoints = EndPoints().endpoints
status_code = StatusCode().status_code
output = Output()
query = Query()


class TeamDetails:
    def __init__(self, team_id):
        """
        :param team_id integer: id of the team
        """
        self._url = endpoints["TeamDetails"]
        self._api_param = {"teamID": team_id}

        self.resp = query.get_stats(url=self._url,
                                    headers=REQ_HEADER,
                                    api_param=self._api_param)
        if self.resp.status_code == status_code["OK"]:
            output.pretty_json(query.convert_to_json())
        else:
            raise Exception("Response is not 200")

    # ToDo: parse the json and return the useful information
    def details(self):
        pass


class CommonTeamRoster:
    # ToDo: league_id: 00 means?, season: current year?
    def __init__(self, team_id, season=CURRENT_SEASON, league_id=LEAGUE_ID):
        """
        :param team_id: id of the team
        :param season: NBA season, String, "2019-20"
        :param league_id: NBA league ID, String
        """

        self._url = endpoints["CommonTeamRoster"]
        self._api_param = {
            "TeamID": team_id,
            "LeagueID": league_id,
            "Season": season
        }

        self.resp = query.get_stats(url=self._url,
                                    headers=REQ_HEADER,
                                    api_param=self._api_param)
        if self.resp.status_code == status_code["OK"]:
            output.pretty_json(query.convert_to_json())
        else:
            raise Exception("Response is not 200")

    # ToDo: parse the json output and return info
    def rosters(self):
        pass


class FranchiseLeaders:
    def __init__(self, team_id):
        """
        :param team_id: id of the team
        """
        self._url = endpoints["FranchiseLeaders"]
        self._api_param = {"TeamID": team_id}

        self.resp = query.get_stats(url=self._url,
                                    headers=REQ_HEADER,
                                    api_param=self._api_param)
        if self.resp.status_code == status_code["OK"]:
            output.pretty_json(query.convert_to_json())
        else:
            raise Exception("Response is not 200")

    def franchise(self):
        pass
