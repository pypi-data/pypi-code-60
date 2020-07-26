from datetime import datetime

_cur_year = datetime.now().year
if datetime.now().month > 6:
    CURRENT_SEASON = str(_cur_year) + "-" + str(_cur_year + 1)[2:]
else:
    CURRENT_SEASON = str(_cur_year - 1) + "-" + str(_cur_year)[2:]

LEAGUE_ID = "00"

class StatusCode:
    def __init__(self):
        self.status_code = {
            "OK": 200,
            "NotExist": 404,
            "InternalError": 500
        }

class EndPoints:
    def __init__(self):
        self.endpoints = {
            "TeamDetails": "https://stats.nba.com/stats/teamdetails?",
            "CommonTeamRoster" : "https://stats.nba.com/stats/commonteamroster?",
            "FranchiseLeaders" : "https://stats.nba.com/stats/franchiseleaders?",
            "CommonTeamYear": "https://stats.nba.com/stats/commonteamyears?"
        }

TEAMS_TO_ID = {
    "AtlantaHawks": 1610612737,
    "BostonCeltics": 1610612738,
    "BrooklynNets": 1610612751,
    "CharlotteHornets": 1610612766,
    "ChicagoBulls": 1610612741,
    "ClevelandCavaliers": 1610612739,
    "DallasMavericks": 1610612742,
    "DenverNuggets": 1610612743,
    "DetroitPistons": 1610612765,
    "GoldenStateWarriors": 1610612744,
    "HoustonRockets": 1610612745,
    "IndianaPacers": 1610612754,
    "Los AngelesClippers": 1610612746,
    "Los AngelesLakers": 1610612747,
    "MemphisGrizzlies": 1610612763,
    "MiamiHeat": 1610612748,
    "MilwaukeeBucks": 1610612749,
    "MinnesotaTimberwolves": 1610612750,
    "NewOrleansPelicans": 1610612740,
    "NewYorkKnicks": 1610612752,
    "OklahomaCityThunder": 1610612760,
    "OrlandoMagic": 1610612753,
    "Philadelphia76ers": 1610612755,
    "PhoenixSuns": 1610612756,
    "PortlandTrailBlazers": 1610612757,
    "SacramentoKings": 1610612758,
    "SanAntonioSpurs": 1610612759,
    "TorontoRaptors": 1610612761,
    "UtahJazz": 1610612762,
    "WashingtonWizards": 1610612764
}
