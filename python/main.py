import pandas as pd
import requests as requests
from bs4 import BeautifulSoup as bs
import os
import time

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
        # tables = soup.find_all('div')

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

for team in teams:
    Team(teams[team]).get_data()
    time.sleep(4)
