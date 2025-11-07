import pandas as pd 
from mcda.core.matrices import PerformanceTable
from mcda.core.scales import *
from mcda.core.functions import *
from mcda.core.criteria_functions import *
from mcda.core.transformers import normalize
from mcda.core.aggregators import WeightedSum

def get_criterias(decision_df: pd.DataFrame) -> list[str]:
    criterias = decision_df.columns.to_list()
    return criterias

def get_alternatives(decision_df: pd.DataFrame) -> list[str]:
    alternatives = decision_df.index.to_list()
    return alternatives

def scale_criteria(criteria_values: pd.Series, preference_direction: str): 
    min = criteria_values.min()
    max = criteria_values.max()
    if preference_direction == "min":
        scale = QuantitativeScale(min, max, preference_direction=MIN)
    else:
        scale = QuantitativeScale(min, max, preference_direction=MAX)
    return scale

def get_scales(criterias: list, scales_list: list):
    scales = dict(zip(criterias, scales_list))
    return scales

def get_performance_table(decision_df: pd.DataFrame,
                          alternatives: list,
                          criterias: list,
                          scales: dict
                          ): 
    performance_table = PerformanceTable(
        data=decision_df,
        alternatives = alternatives,
        criteria = criterias,
        scales=scales
    )
    if not performance_table.is_within_scales:
        raise ValueError("Some values are out of the defined scales")
    return performance_table

def define_value_function(segments: list):
    vf = PieceWiseFunction(segments=segments) 
    return vf

def associate_value_functions(criterias: list, functions_list: list, scales: dict): 
    functions = dict(zip(criterias, functions_list))
    in_scales = {criteria: scales[criteria] for criteria in criterias}
    value_functions = CriteriaFunctions(
        functions=functions,
        in_scales=in_scales
    )
    return value_functions

def compute_values_table(performance_table, value_functions):
    values_table = value_functions(performance_table)
    return values_table

def normalize_weights(weights: pd.Series):
    normalized_weights = weights / weights.sum()
    return normalized_weights

def compute_weighted_sum(values_table, normalized_weights: pd.Series):
    weighted_sum = WeightedSum(normalized_weights)
    alternatives_scores = weighted_sum(values_table)
    alternatives_scores = alternatives_scores.data.sort_values(ascending=False)
    return alternatives_scores

def get_best_alternatives(alternatives_scores,
                          initial_df: pd.DataFrame,
                          column_index: str,
                          n_alternives: int
                          ):
    indexes = alternatives_scores[0:len(alternatives_scores)-2][:n_alternives]
    best_alternatives = initial_df.loc[initial_df[column_index].isin(indexes.index)]
    return best_alternatives

 








