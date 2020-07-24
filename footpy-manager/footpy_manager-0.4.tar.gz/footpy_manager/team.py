class Team:

    def __init__(self, name, country=""):
        """
        Def:
        This function is executed when a team is initialized. The ID was created to identify duplicate teams.

        Args:
            name (str): The name of the team.
            country (str, optional): The country of the team. Defaults to "".
        """
        self.name = name
        self.country = country
        self.id = str(name).lower().strip()

    def set_country(self, country):
        '''
        This function able to change the country of the team.
        '''
        self.country = country