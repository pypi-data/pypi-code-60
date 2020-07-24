import pandas as pd

class FootpyManager:

    def __init__(self):
        self.teams = pd.DataFrame(columns=["id", "name", "country"])
        self.matches = pd.DataFrame(
            columns=["home_id", "home_name", "home_score",
                     "away_id", "away_name", "away_score",
                     "goals_total", "goals_difference", "winner",
                     "date"]
            )

    def insert_match(self, match):
        """
        Def:
        This function insert a match in the manager and insert the teams in the dataframe of teams.

        Args:
            match ([object Match]): The register of the match
        """
        has_home_team = False
        has_away_team = False

        for index, team in self.teams.iterrows():
            if team.id == match.home_team.id: has_home_team = True
            if team.id == match.away_team.id: has_away_team = True

        if (has_home_team == False): self.insert_team(match.home_team)
        if (has_away_team == False): self.insert_team(match.away_team)

        self.matches = self.matches.append({
            'home_id': match.home_team.id,
            'home_name': match.home_team.name,
            'home_score': match.home_score,
            'away_id': match.away_team.id,
            'away_name': match.away_team.name,
            'away_score': match.away_score,
            'goals_total': match.goals_total,
            'goals_difference': match.goals_difference,
            'winner': match.winner.name if (match.winner != None) else None,
            'date': match.date,
            'object': match
        }, ignore_index=True)

    def insert_team(self, team):
        """
        Def:
        This function insert a team in the dataframe.

        Args:
            team ([object Team]): The register of the team
        """
        self.teams = self.teams.append({
            'id': team.id,
            'name': team.name,
            'country': team.country
        }, ignore_index=True)

    def match_with_more_goals(self, team=None):
        """
        Def:
        This function return the match with the most goals in the total. If a team is inputted
        the function filter the matches of this team.

        Args:
            team ([object Team], optional): Filters the matches of a team. Defaults to None.

        Returns:
            [object Match]: The match with the most goals in total
        """
        matches = self.matches
        if(team != None):
            matches = self.matches.query("home_id == '"+team.id+"' | away_id == '"+team.id+"'")

        return matches.sort_values(by='goals_total', ascending=False).head(1).object.item()

    def match_with_most_difference_goals(self, team=None):
        """
        Def:
        This function return the match with the most difference of goals. If a team is inputted
        the function filter the matches of this team.

        Args:
            team ([object Team], optional): Filters the matches of a team. Defaults to None.

        Returns:
            [object Match]: The match with the most difference of goals
        """
        matches = self.matches
        if(team != None):
            matches = self.matches.query("home_id == '"+team.id+"' | away_id == '"+team.id+"'")

        return matches.sort_values(by='goals_difference', ascending=False).head(1).object.item()

    def mean_goals_made(self, team):
        """
        Def:
        This function return the mean of goals made by the team inputted.

        Args:
            team ([object Team]): The team to be analyzed.

        Returns:
            [float]: The mean of goals made by the team selected.
        """
        matches_filtered = self.matches.query("home_id == '"+team.id+"' | away_id == '"+team.id+"'")
        home_score_mean = matches_filtered[matches_filtered['home_id'] == team.id]['home_score'].sum()
        away_score_mean = matches_filtered[matches_filtered['away_id'] == team.id]['away_score'].sum()

        return (home_score_mean + away_score_mean) / matches_filtered.shape[0]

    def mean_goals_suffered(self, team):
        """
        Def:
        This function return the mean of goals suffered by the team inputted.

        Args:
            team ([object Team]): The team to be analyzed.

        Returns:
            [float]: The mean of goals suffered by the team selected.
        """
        matches_filtered = self.matches.query("home_id == '"+team.id+"' | away_id == '"+team.id+"'")
        home_score_mean = matches_filtered[matches_filtered['home_id'] == team.id]['away_score'].sum()
        away_score_mean = matches_filtered[matches_filtered['away_id'] == team.id]['home_score'].sum()

        return (home_score_mean + away_score_mean) / matches_filtered.shape[0]
