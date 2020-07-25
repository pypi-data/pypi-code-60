import requests
import pprint
import constants
from python_nbaclient import REQ_HEADER


class TeamDetails:
    def __init__(self, team_id):
        # ToDo: use constants.py, so that having one place to update all constants
        self._url = constants.TEAM_DETAILS_URI
        self._api_param = {"teamID": team_id}
        # ToDo: either use a constant or https://httpbin.org/user-agent
        self._headers = REQ_HEADER
        response = requests.get(self._url,
                                headers=self._headers,
                                params=self._api_param)
        if response.status_code == 200:
            self.team_details = response.json()
            pp = pprint.PrettyPrinter(indent=4)
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
        :param league_id: NBA leangue ID, String
        """
        # ToDo: same as above, constant
        self._url = "https://stats.nba.com/stats/commonteamroster?"
        self._api_param = {
            "TeamID": team_id,
            "LeagueID": league_id,
            "Season": season
        }
        # ToDo: this might be a global variable?
        self._headers = {
            "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }

        response = requests.get(self._url,
                                headers=self._headers,
                                params=self._api_param)
        if response.status_code == 200:
            self.team_roster = response.json()
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
        self._url = "https://stats.nba.com/stats/franchiseleaders?"
        self._api_param = {"TeamID": team_id}
        self._headers = {
            "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }

        response = requests.get(self._url,
                                headers=self._headers,
                                params=self._api_param)
        if response.status_code == 200:
            self.franchise_leader = response.json()
        else:
            print("Error")

    def franchise(self):
        pass

