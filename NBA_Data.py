import requests
import pandas as pd
from bs4 import BeautifulSoup
import time;

url = 'https://www.basketball-reference.com/leagues/NBA_2024_standings.html'
all_teams = []
data = requests.get(url)
soup = BeautifulSoup(data.content, 'html.parser')
teams_table = soup.select('table.stats_table')[0]
links = teams_table.findAll('a')
teams_table2 = soup.select('table.sortable')[1]
links2 = teams_table2.findAll('a')
combined_links = links + links2
combined_links = [l.get('href') for l in combined_links]
combined_links = [l for l in combined_links if '/teams/' in l]
teams = [f"https://basketball-reference.com{l}" for l in combined_links]
for team_url in teams:
    team_name = team_url.replace("/2024.html", "").split("/")[-1]
    team_data = requests.get(team_url)
    per_game = pd.read_html(team_data.text, match="Per Game")[0]
    per_game["Team"] = team_name
    country = pd.read_html(team_data.text, match="Roster")[0]
    allStats = per_game.merge(country[["Player","Pos", "Birth", "College"]], on="Player")
    allStats['Birth'] = allStats['Birth'].str.split().str[-1]
    all_teams.append(allStats)
    time.sleep(5)

stat_df = pd.concat(all_teams)
stat_df = stat_df.drop(columns=['Rk'])
cols = list(stat_df.columns)
if 'Pos' in cols:
    cols.remove('Pos')
    cols.insert(1, 'Pos')

stat_df = stat_df[cols]
stat_df.to_csv("nbaStats.csv", index=False, encoding='utf-8')







