import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

team_name_mapping = {
    'BOS': 'Boston Celtics',
    'ATL': 'Atlanta Hawks',
    'BRK': 'Brooklyn Nets',
    'CHO': 'Charlotte Hornets',
    'CHI': 'Chicago Bulls',
    'CLE': 'Cleveland Cavaliers',
    'DAL': 'Dallas Mavericks',
    'DEN': 'Denver Nuggets',
    'DET': 'Detroit Pistons',
    'GSW': 'Golden State Warriors',
    'HOU': 'Houston Rockets',
    'IND': 'Indiana Pacers',
    'LAC': 'LA Clippers',
    'LAL': 'Los Angeles Lakers',
    'MEM': 'Memphis Grizzlies',
    'MIA': 'Miami Heat',
    'MIL': 'Milwaukee Bucks',
    'MIN': 'Minnesota Timberwolves',
    'NOP': 'New Orleans Pelicans',
    'NYK': 'New York Knicks',
    'OKC': 'Oklahoma City Thunder',
    'ORL': 'Orlando Magic',
    'PHI': 'Philadelphia 76ers',
    'PHO': 'Phoenix Suns',
    'POR': 'Portland Trail Blazers',
    'SAC': 'Sacramento Kings',
    'SAS': 'San Antonio Spurs',
    'TOR': 'Toronto Raptors',
    'UTA': 'Utah Jazz',
    'WAS': 'Washington Wizards'
}

url = 'https://www.basketball-reference.com/leagues/NBA_2024_standings.html'
all_teams = []
data = requests.get(url)
data.encoding = 'utf-8'
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
    team_abbr = team_url.replace("/2024.html", "").split("/")[-1]
    team_name = team_name_mapping.get(team_abbr, team_abbr)
    team_data = requests.get(team_url)
    team_data.encoding = 'utf-8'
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
stat_df.to_csv("nbaStats.csv", index=False, encoding='utf-8-sig')








