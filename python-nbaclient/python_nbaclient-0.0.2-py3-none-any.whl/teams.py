import requests
import pprint
from python_nbaclient import REQ_HEADER, constants


class TeamDetails:
    def __init__(self, team_id):
        """
        :param team_id: id of the team
        """
        self._url = constants.TEAM_DETAILS_URI
        self._api_param = {"teamID": team_id}
        self._headers = REQ_HEADER
        response = requests.get(self._url,
                                headers=self._headers,
                                params=self._api_param)
        if response.status_code == 200:
            self.team_details = response.json()
            pp = pprint.PrettyPrinter(indent=2)
            pp.pprint(self.team_details)
        else:
            # ToDo: Error Log and a generic way of handling error
            print("Error")

    # ToDo: parse the json and return the useful information
    def details(self):
        pass


class CommonTeamRoster:
    # ToDo: league_id: 00 means?, season: current year?
    def __init__(self, team_id, season, league_id="00"):
        """
        :param team_id: id of the team
        :param season: NBA season, String, "2019-20"
        :param league_id: NBA league ID, String
        """

        self._url = constants.COMMON_TEAM_ROSTER_URI
        self._api_param = {
            "TeamID": team_id,
            "LeagueID": league_id,
            "Season": season
        }

        self._headers = REQ_HEADER

        response = requests.get(self._url,
                                headers=self._headers,
                                params=self._api_param)
        if response.status_code == 200:
            self.team_roster = response.json()
            pp = pprint.PrettyPrinter(indent=2)
            pp.pprint(self.team_roster)
        else:
            print("Error")

    # ToDo: parse the json output and return info
    def rosters(self):
        pass


class FranchiseLeaders:
    def __init__(self, team_id):
        """
        :param team_id: id of the team
        """
        self._url = constants.FRANCHISE_LEADER_URI
        self._api_param = {"TeamID": team_id}
        self._headers = REQ_HEADER

        response = requests.get(self._url,
                                headers=self._headers,
                                params=self._api_param)
        if response.status_code == 200:
            self.franchise_leader = response.json()
            pp = pprint.PrettyPrinter(indent=2)
            pp.pprint(self.franchise_leader)
        else:
            print("Error")

    def franchise(self):
        pass
