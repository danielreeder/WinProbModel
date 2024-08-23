import pandas as pd
import requests as requests
from bs4 import BeautifulSoup as bs
import os

class Team:
    def __init__(self, name, path=''):
        self.name = name
        self.path = path

    def get_data(self):
        self.path = rf'C:\Users\danie\Desktop\Portfolio Projects\WinProbModel\data\{self.name}'

        if not os.path.exists(self.path):
            os.makedirs(self.path) 
            
        r = requests.get(f'https://www.baseball-reference.com/teams/{self.name}/2024.shtml')

        print(f"Retrieving data for {self.name}")
        print("Data grabbed")

        soup = bs(r.content, 'html.parser')
        
        tables = soup.find_all('div', class_='table_wrapper')

        batting_header, batting_data = self.parse_data(tables[0])
        pitching_header, pitching_data = self.parse_data(tables[1])

        batting = self.clean_data(pd.DataFrame(data=batting_data, columns=batting_header))
        pitching = self.clean_data(pd.DataFrame(data=pitching_data, columns=pitching_header))

        batting.to_csv(f'{self.path}/batting.csv', index=False)
        pitching.to_csv(f'{self.path}/pitching.csv', index=False)
        print("Data exported\n")

    def parse_data(self, data):
        table = data.find('table')
        data = table.find_all("tr")

        header_list = data[0]
        header = []
        data_list = data[1:]
        data = []

        for title in header_list:
            try: 
                text = title.get_text()
                if text != '\n':
                    header.append(text)
            except: 
                continue

        for element in data_list:
            temp_data = []
            try:
                for sub_element in element:
                    text = sub_element.get_text()
                    if text != '\n' and text != '':
                        temp_data.append(text)

            except: 
                continue

            data.append(temp_data)
        return header, data

    def clean_data(self, data : pd.DataFrame):
        cleaned = data.query("Rk != 'Rk'").iloc[:, 1:].dropna()
        cleaned.Name = cleaned.Name.apply(lambda x: x.strip('*#+'))
        cleaned.Name = cleaned.Name.apply(lambda x: x.split('(')[0])
        print("Cleaned")
        return cleaned

teams = {
    "Arizona Diamondbacks": "ARI",
    "Atlanta Braves": "ATL",
    "Baltimore Orioles": "BAL",
    "Boston Red Sox": "BOS",
    "Chicago Cubs": "CHC",
    "Chicago White Sox": "CHW",
    "Cincinnati Reds": "CIN",
    "Cleveland Guardians": "CLE",
    "Colorado Rockies": "COL",
    "Detroit Tigers": "DET",
    "Miami Marlins": "MIA",
    "Houston Astros": "HOU",
    "Kansas City Royals": "KCR",
    "Los Angeles Angels": "LAA",
    "Los Angeles Dodgers": "LAD",
    "Milwaukee Brewers": "MIL",
    "Minnesota Twins": "MIN",
    "New York Mets": "NYM",
    "New York Yankees": "NYY",
    "Oakland Athletics": "OAK",
    "Philadelphia Philles": "PHI",
    "Pittsburgh Pirates": "PIT",
    "San Diego Padres": "SDP",
    "San Francisco Giants": "SFG",
    "Seattle Mariners": "SEA",
    "St. Louis Cardinals": "STL",
    "Tampa Bay Rays": "TBR",
    "Texas Rangers": "TEX",
    "Toronto Blue Jays": "TOR",
    "Washington Nationals": "WAS"
}

def calculate_probability(prob_of_reaching, prob_of_next):
    return prob_of_reaching * prob_of_next

def calculate_win_probability(inning, outs, home_team, away_team, home_score, away_score, bases):
    home_batting = pd.read_csv(f'data/{home_team}/batting.csv')
    away_batting = pd.read_csv(f'data/{away_team}/batting.csv')
    home_pitching = pd.read_csv(f'data/{home_team}/pitching.csv')
    away_pitching = pd.read_csv(f'data/{away_team}/pitching.csv')

    home_lineup = home_batting.iloc[:9, :]
    away_lineup = away_batting.iloc[:9, :]
    return calculate_win_probability_wrapper(inning, outs, bases, home_score, away_score, home_lineup, away_lineup, 0, home_pitching.iloc[0, :], 1, 1)


""" BASES """
""" 1 : 000 """
""" 2 : 001 """
""" 3 : 010 """
""" 4 : 011 """
""" 5 : 100 """
""" 6 : 101 """
""" 7 : 110 """
""" 8 : 111 """
def calculate_win_probability_wrapper(inning : int, outs : int, bases : list, home_score : int, away_score : int, home_lineup : list, away_lineup : list, batter : int, pitcher : str, current_probability : float, next_action_probability : float):
    if current_probability < 1e-4:
        return current_probability * next_action_probability * int(home_score > away_score) 
    
    current_probability *= next_action_probability
    cumulative_win_probability = 0.0
    
    lineup = home_lineup if inning % 2 == 0 else away_lineup

    current_batter = lineup.loc[batter]
    next_batter = (batter + 1) % 9

    # SINGLE

    # DOUBLE

    # TRIPLE

    # HOME RUN
    homerun_probability = current_batter["HR"] / current_batter["PA"]
    batter_name = current_batter["Name"]
    print(f"{batter_name}: Homerun")
    if inning % 2 == 0:
            home_score += sum(bases) + 1
    else: 
        away_score += sum(bases) + 1
    bases = [0, 0, 0]
    cumulative_win_probability += calculate_win_probability_wrapper(inning, outs, bases, home_score, away_score, home_lineup, away_lineup, next_batter, pitcher, current_probability, homerun_probability)
    print(cumulative_win_probability)
    # STRIKEOUT
    strikeout_probability = current_batter["SO"] / current_batter["PA"]
    print(f"{batter_name}: Strikeout")

    if outs == 2:
        inning += 1
        outs = 0
        bases = [0, 0, 0]
    else:
        outs += 1
    cumulative_win_probability += calculate_win_probability_wrapper(inning, outs, bases, home_score, away_score, home_lineup, away_lineup, next_batter, pitcher, current_probability, strikeout_probability)

    # FLYOUT
    flyout_probability = 0.0005
    print(f"{batter_name}: Flyout")
    if bases[0] == 1:
        bases[0] = 0
        if inning % 2 == 0:
            home_score += 1
        else: 
            away_score += 1
    
    if bases[1] == 1:
        bases[0] = 1
    
    if outs == 2:
        inning += 1
        outs = 0
        bases = [0, 0, 0]
    
    cumulative_win_probability += calculate_win_probability_wrapper(inning, outs, bases, home_score, away_score, home_lineup, away_lineup, next_batter, pitcher, current_probability, flyout_probability)

    # GB OUT
    gbout_probability = 0.0005
    print(f"{batter_name}: gbout")
    if bases[0] == 1: 
        if inning % 2 == 0:
            home_score += 1
        else: 
            away_score += 1 
    
    return cumulative_win_probability * int(home_score > away_score)



print(calculate_win_probability(0, 0, 'PHI', 'WSN', 0, 0, [0, 0, 0]))

