import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
from functools import reduce
from football_recruitement_tool.paths import path_to_raw_data, path_to_results
import football_recruitement_tool.mavt as mavt
from football_recruitement_tool.config_value_functions import value_functions_segments_per_dm
from football_recruitement_tool.config_weights import weights_dict

################
### GET DATA ###
################
players_df = pd.read_csv(path_to_raw_data, sep=";", encoding="latin1")

#####################
### PREPROCESSING ###
#####################
### Common preprocessing for decision-makers ###
strikers_df = players_df.copy()
strikers_df = strikers_df.loc[(strikers_df['Values'] < 15000000) & (strikers_df['Salary'] < 50000)]
strikers_df = strikers_df.loc[strikers_df['Position'] == 'S']
strikers_df = strikers_df.drop(columns=["Position"])
strikers_df = strikers_df.loc[(strikers_df['Age'] <= 35) & (strikers_df['Age'] >= 20)]
strikers_df = strikers_df.set_index('UID', drop=False)
strikers_df = strikers_df.drop('UID', axis=1)

###########################
### FEATURE ENGINEERING ###
###########################
### Feature Selection for the first decision-maker ###
strikers_1 = strikers_df.copy()
col_to_keep_1 = ['Age','Finishing','Heading','Dribbling','Teamwork','Ambition','Loyal','Natural Fitness','Injury']
strikers_1 = strikers_1[col_to_keep_1]
strikers_1 = strikers_1.loc[strikers_1['Finishing'] >= 10]

### Feature Selection for the second decision-maker ###
strikers_2 = strikers_df.copy()
col_to_keep_2 = ['Age', 'Values', 'Salary', 'ca', 'Sportsmanship', 'Emotional control', 'Loyal', 'Ambition', 'World reputation']
strikers_2 = strikers_2[col_to_keep_2]

strikers_dfs = [strikers_1, strikers_2]

##################################
### Multi-criterias evaluation ###
##################################
preference_directions = {
    'Age': 'min',
    'Values': 'max',
    'Salary': 'min',
    'ca': 'max',
    'Sportsmanship': 'max',
    'Emotional control': 'max',
    'Loyal': 'max',
    'Ambition': 'max',
    'World reputation': 'max',
    'Finishing': 'max',
    'Heading': 'max',
    'Dribbling': 'max',
    'Teamwork': 'max',
    'Natural Fitness': 'max',
    'Injury': 'min'
}

alternatives_dict = {}
criterias_dict = {}
alternatives_scores_dict = {}
for idx, df in enumerate(strikers_dfs, start=1): 
    alternatives_dict[idx] = mavt.get_alternatives(decision_df=df)
    criterias_dict[idx] = mavt.get_criterias(decision_df=df)
    criterias, alternatives = criterias_dict[idx], alternatives_dict[idx]
    scales_list = [
        mavt.scale_criteria(
            criteria_values=df[criteria],
            preference_direction=preference_directions[criteria])
            for criteria in criterias
            ]
    scales = mavt.get_scales(
        criterias=criterias,
        scales_list=scales_list
    )

    performance_table = mavt.get_performance_table(
        decision_df=df,
        alternatives=alternatives,
        criterias=criterias,
        scales=scales
    )

    functions_list = [
        mavt.define_value_function(
            value_functions_segments_per_dm[idx][criteria]
        ) for criteria in criterias            
    ]

    value_functions = mavt.associate_value_functions(
        criterias=criterias,
        functions_list=functions_list,
        scales=scales
    )

    values_table = mavt.compute_values_table(
        performance_table=performance_table,
        value_functions=value_functions
    )

    weights = pd.Series(weights_dict[idx])
    normalized_weights = mavt.normalize_weights(weights=weights)
    alternatives_scores = mavt.compute_weighted_sum(
        values_table=values_table,
        normalized_weights=normalized_weights
    )
    alternatives_scores_dict[idx] = alternatives_scores

    best_alternatives = mavt.get_best_alternatives(
        alternatives_scores=alternatives_scores, 
        initial_df=players_df,
        column_index='UID',
        n_alternives=10 #arbitrary choice
    )

    print(f'the selected alternatives for the decision-maker {idx} are {best_alternatives['Name']}')

### Final choice – implementing the compromise ###
dfs = []
for idx, scores in alternatives_scores_dict.items():
    df = scores.reset_index()
    df.columns = ['UID', f'score_dm{idx}']
    dfs.append(df)

global_standings = reduce(lambda left, right: pd.merge(left, right, on='UID'), dfs)

score_cols = [col for col in global_standings.columns if col.startswith('score_dm')]
global_standings['global_score'] = global_standings[score_cols].sum(axis=1)

sorted_global_standings = global_standings.sort_values(by='global_score', ascending=False)

top_players = pd.merge(
    sorted_global_standings,
    players_df[['UID', 'Name']],
    left_on='UID',
    right_on='UID'
)
top_players = top_players[['Name', 'global_score']]

top_players.to_csv(path_to_results, index=False)
print(f"Top players csv saved in {path_to_results}")
print(top_players.head(10))












    
    

    









