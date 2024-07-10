import pandas as pd
import numpy as np
import random as rdm
# Set the display option to show all columns without truncation
pd.options.display.max_columns = None

class Team:
    def __init__(self, name, abv, overall, country):
        self.name = name
        self.abv = abv
        self.overall = overall
        self.country = country


class League:
    def __init__(self, name, teams):
        self.name = name
        self.teams = teams
        self.weeks = []

        data = []
        for team in teams:
            data.append({
                'Team Name': team.name,
                'Games Played': 0,  # Initialize to 0 or any default value
                'Victories': 0,
                'Draws': 0,
                'Losses': 0,
                'Goals Scored': 0,
                'Goals Against': 0,
                'Goal Differential': 0,
                'Points': 0
            })

        # Create the DataFrame

        df = pd.DataFrame(data)
        df.index = range(1, len(df) + 1)
        self.classification = df
    '''
    def classification(self):
        for week in self.weeks:
            for game in week:
    '''


    def show_all_results(self):
        for week, games in enumerate(self.weeks, start=1):
            print(f"-------Week {week}-------")
            print()
            for game in games:
                print(f"{game.home_team.name} {game.home_goals} - {game.away_goals} {game.away_team.name}")
            print()

    def sim_all_league(self):
        for week, games in enumerate(self.weeks, start=1):
            print(f"-------Week {week}-------")
            print()
            for game in games:
                game.playGame()
                print(f"{game.home_team.name} {game.home_goals} - {game.away_goals} {game.away_team.name}")


                home_row_index = self.classification[self.classification['Team Name'] == game.home_team.name].index[0]
                away_row_index = self.classification[self.classification['Team Name'] == game.away_team.name].index[0]
                self.classification.loc[home_row_index, 'Games Played'] += 1
                self.classification.loc[home_row_index, 'Goals Scored'] += game.home_goals
                self.classification.loc[home_row_index, 'Goals Against'] += game.away_goals
                home_diff = game.home_goals - game.away_goals
                self.classification.loc[home_row_index, 'Goal Differential'] += home_diff

                self.classification.loc[away_row_index, 'Games Played'] += 1
                self.classification.loc[away_row_index, 'Goals Scored'] += game.away_goals
                self.classification.loc[away_row_index, 'Goals Against'] += game.home_goals
                away_diff = game.away_goals - game.home_goals
                self.classification.loc[away_row_index, 'Goal Differential'] += away_diff

                if game.result() == game.home_team:
                    self.classification.loc[home_row_index, 'Victories'] += 1
                    self.classification.loc[away_row_index, 'Losses'] += 1
                    self.classification.loc[home_row_index, 'Points'] += 3

                elif game.result() == game.away_team:
                    self.classification.loc[away_row_index, 'Victories'] += 1
                    self.classification.loc[home_row_index, 'Losses'] += 1
                    self.classification.loc[away_row_index, 'Points'] += 3
                else:
                    self.classification.loc[home_row_index, 'Draws'] += 1
                    self.classification.loc[away_row_index, 'Draws'] += 1
                    self.classification.loc[home_row_index, 'Points'] += 1
                    self.classification.loc[away_row_index, 'Points'] += 1
        print()

    def sim_week(self):
        print()


    def create_balanced_round_robin(self):
        """ Create a schedule for the players in the list and return it"""
        s = []
        if len(self.teams) % 2 == 1: self.teams = self.teams + [None]
        # manipulate map (array of indexes for list) instead of list itself
        # this takes advantage of even/odd indexes to determine home vs. away
        n = len(self.teams)
        map = list(range(n))
        mid = n // 2
        for i in range(n - 1):
            l1 = map[:mid]
            l2 = map[mid:]
            l2.reverse()
            round = []

            for j in range(mid):
                t1 = self.teams[l1[j]]
                t2 = self.teams[l2[j]]

                if j == 0 and i % 2 == 1:
                    # flip the first match only, every other round
                    # (this is because the first match always involves the last player in the list)
                    round.append(Game(t2, t1))
                else:
                    round.append(Game(t1, t2))
            self.weeks.append(round)
            # rotate list by n/2, leaving last element at the end
            map = map[mid:-1] + map[:mid] + map[-1:]

        rdm.shuffle(self.weeks)
        for week in self.weeks:
            rdm.shuffle(week)

        # Second Volta
        weeks = self.weeks.copy()
        for week in weeks:
            round = []
            for game in week:
                round.append(Game(game.away_team, game.home_team))
            self.weeks.append(round)


        return self.weeks





class Game:
    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.home_goals = 0
        self.away_team = away_team
        self.away_goals = 0
        self.flag = False

    def playGame(self):

        # Overall Difference
        away_multiplier = self.home_team.overall**3 / self.away_team.overall**3
        home_multiplier = self.away_team.overall**3 / self.home_team.overall**3
        base_chance_goal = 13
        #print(home_multiplier)
        #print(away_multiplier)

        first_half_add_time = rdm.randint(0, 5)
        for i in range(0, 46 + first_half_add_time):
            r1 = rdm.randint(0, 1000)
            b1 = base_chance_goal*away_multiplier
            r2 = rdm.randint(0, 1000)
            b2 = base_chance_goal*home_multiplier

            #print(f"r1:{r1}, b1:{b1}, r2:{r2}, b2:{b2}")

            if r1 < b1:
                self.home_goals += 1
                #print("Home Goal")
            if r2 < b2:
                self.away_goals += 1
                #print("Away Goal")

        #print()
        second_half_add_time = rdm.randint(0, 9)
        for i in range(45, 91 + second_half_add_time):
            r1 = rdm.randint(0, 1000)
            b1 = base_chance_goal * away_multiplier
            r2 = rdm.randint(0, 1000)
            b2 = base_chance_goal * home_multiplier

            #print(f"r1:{r1}, b1:{b1}, r2:{r2}, b2:{b2}")

            if r1 < b1:
                self.home_goals += 1
                #print("Home Goal")
            if r2 < b2:
                self.away_goals += 1
                #print("Away Goal")

        self.flag = True
        return self.home_goals, self.away_goals



    def result(self):
        if self.home_goals > self.away_goals:
            return self.home_team
        elif self.away_goals > self.home_goals:
            return self.away_team
        else:
            return None


SLB = Team("SL Benfica", "SLB", 81, "Portuguese")
FCP = Team("FC Porto", "FCP", 79, "Portuguese")
SCB = Team("SC Braga", "SCB", 75, "Portuguese")
SCP = Team("Sporting CP", "SCP", 84, "Portuguese")
FCA = Team("FC Arouca", "FCA", 69, "Portuguese")
VSC = Team("Vitória SC", "VSC", 70, "Portuguese")
GDC = Team("GD Chaves", "GDC", 66, "Portuguese")
FCF = Team("FC Famalicão", "FCF", 69, "Portuguese")
BFC = Team("Boavista FC", "BFC", 67, "Portuguese")
CPAC = Team("Casa Pia AC", "CSP", 68, "Portuguese")
FCV = Team("FC Vizela", "FCV", 65, "Portuguese")
RAFC = Team("Rio Ave FC", "RAV", 65, "Portuguese")
GVFC = Team("Gil Vicente FC", "GVC", 65, "Portuguese")
GDEP = Team("GD Estoril Praia", "ETP", 64, "Portuguese")
PSC = Team("Portimonense SC", "PSC", 63, "Portuguese")
MFC = Team("Moreirense FC", "MFC", 62, "Portuguese")
SCF = Team("SC Farense", "SCF", 62, "Portuguese")
CFE = Team("CF Estrela", "CFE", 62, "Portuguese")


INT = Team("Internazionale Milano", "INT", 87, "Italian")
RSC = Team("Real Sociedad", "RSC", 81, "Spanish")
RBS = Team("Red Bull Salzburg", "RBS", 76, "Austrian")


portuguese_teams = [SLB, FCP, SCB, SCP, FCA, VSC, GDC, FCF, BFC, CPAC, FCV, RAFC, GVFC, GDEP, PSC, MFC, SCF, CFE]
liga = League("Liga Portuguesa", portuguese_teams)
liga.create_balanced_round_robin()
liga.sim_all_league()
classification = liga.classification.sort_values(by=["Points", "Goal Differential"], ascending=False)
classification.index = range(1, len(classification) + 1)
print(classification)
#liga.show_all_results()




