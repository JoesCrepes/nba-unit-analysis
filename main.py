import plotly.graph_objects as go

teamsets = [
    ['ATL'],
    ['BOS'],
    ['NJN'],
    ['CHA'],
    ['CHI'],
    ['CLE'],
    ['DAL'],
    ['DEN'],
    ['DET'],
    ['GSW'],
    ['HOU'],
    ['IND'],
    ['LAC',],
    ['LAL',],
    ['MEM'],
    ['MIA'],
    ['MIL'],
    ['MIN'],
    ['NOH'],
    ['NYK'],
    ['OKC'],
    ['ORL'],
    ['PHI'],
    ['PHO'],
    ['POR'],
    ['SAC'],
    ['SAS'],
    ['TOR'],
    ['UTA'],
    ['WAS']
    ]


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from unicodedata import normalize

# test = pd.read_html('https://www.basketball-reference.com/teams/NJN/#NJN')[0]
# test2 = pd.read_html('https://www.basketball-reference.com/teams/OKC/#OKC')[0]
# concat = pd.concat([test, test2])
# concat
baseurl = 'https://www.basketball-reference.com/teams/'

for team in teamsets:
  url = baseurl + team[0] + "/#" + team[0]
  time.sleep(5)
  teamstats = pd.read_html(url)
  teamstatsdf = teamstats[0]
  teamstatsdf['shortname'] = team[0]
  if team[0] == 'ATL':
    allteamstats = teamstatsdf
  else:
    allteamstats = pd.concat([allteamstats, teamstatsdf])
    

allteamstats['RoundedSRS'] = allteamstats['SRS']
formattedteamstats = allteamstats.round({'RoundedSRS': 0})
formattedteamstats['RoundedSRS'] = formattedteamstats['RoundedSRS'] + 15

formattedteamstats['RoundedSRS'].max()

formattedteamstats['SeasonTeam'] = formattedteamstats['Season'] + ' ' + formattedteamstats['Team']
formattedteamstats['City'] = formattedteamstats['Team'].str.split(' ').str[0]

currentseasonstats = formattedteamstats[formattedteamstats['Season'] == '2024-25']
historicalstats = formattedteamstats[formattedteamstats['Season'] != '2024-25']

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=historicalstats['Rel DRtg'],
        y=historicalstats['Rel ORtg'],
        mode='markers',
        name='Historic',
        showlegend=True,
        opacity=0.25,
        customdata=np.stack((historicalstats['SRS'], historicalstats['Team'], historicalstats['Season']), axis=-1),
        marker=dict(
            size=historicalstats['RoundedSRS'],
            sizemode='area',
            sizeref=.1,
        ),
            
    )
)

fig.add_trace(
    go.Scatter(
        x=currentseasonstats['Rel DRtg'],
        y=currentseasonstats['Rel ORtg'],
        mode='markers',
        name='2024-25',
        showlegend=True,
        customdata=np.stack((currentseasonstats['SRS'], currentseasonstats['Team'], currentseasonstats['Season']), axis=-1),
        marker=dict(
            size=currentseasonstats['RoundedSRS'],
            sizemode='area',
            sizeref=.1,
        ),
        text=currentseasonstats['shortname'],
        textposition='top center'
    )
)
fig.update_xaxes(range=[12,-12]),
fig.update_yaxes(range=[-12,12]),

fig.update_layout(
    title='Relative Offensive vs. Defensive Rating for NBA Teams',
    xaxis_title='Relative Defensive Rating',
    yaxis_title='Relative Offensive Rating',
    height=1000,
    width=1000,
    font_family="Arial"
    # hovermode='closest',
)

fig.update_traces(
    hovertemplate = 
    '<b>%{customdata[2]} %{customdata[1]}</b><br>' +
    'Relative DRtg: %{x:.2f}<br>' +
    'Relative ORtg: %{y:.2f}<br>' +
    'SRS: %{customdata[0]}<br>',
    mode='markers+text',
)

fig.show()

# fig.write_html("export.html")
