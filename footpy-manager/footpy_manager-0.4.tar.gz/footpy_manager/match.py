from .team import Team

class Match:

    def __init__(self, home_team, away_team, home_score=0, away_score=0, date="00-00-0000"):
        """
        Def:
        This is the function of initialization of a match.

        Args:
            home_team ([object Team]): The home team of the match.
            away_team ([object Team]): The away team of the match.
            home_score (int, optional): The score of the home team. Defaults to 0.
            away_score (int, optional): The score of the away team. Defaults to 0.
            date (str, optional): The date of the match. Defaults to "00-00-0000".
        """
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = home_score
        self.away_score = away_score
        self.date = date

        self.goals_total = home_score + away_score
        self.goals_difference = abs(home_score - away_score)

        self.winner = self.define_winner()

    def __repr__(self):
        """
        Def:
        This function rewrite the representation default of the Python, so this function will be executed
        when the object will printed.
        """
        text = "{} ({}) x ({}) {} ({}) \n\n".format(self.home_team.name, self.home_score, self.away_score, self.away_team.name, self.date)

        if(self.winner != None):
            text += "The winner was {} with {} goals of difference.".format(self.winner.name, self.goals_difference)
        else:
            text += "The match ended drew."

        return text

    def define_winner(self):
        """
        Def:
        This function return which team won the match

        Returns:
            [object Team]: The winner team, if the match ended drew the value returned is None
        """
        if ( self.home_score > self.away_score ):
            return self.home_team
        elif ( self.home_score == self.away_score ):
            return None
        else:
            return self.away_team