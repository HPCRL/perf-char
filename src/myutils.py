import pandas as pd


def xnor(a, b):
    return (a == b)


def sum_lists(list1, list2):
    result = []
    for elem1, elem2 in zip(list1, list2):
        result.append(elem1 + elem2)
    return result


def make_bot_top(pivot, mask1, mask2):
    bot = sum_lists(pivot[:5], mask1)
    top = sum_lists(pivot[:5], mask2)
    return bot, top


def compare_three(pivot, bot, top, points: pd.DataFrame):
    #ignore = 0
    localmin = 0
    #nonmin = 0
    invalid = 0
    neighbours_invalid = 0
    bot_conf = bot
    top_conf = top
    condition_bot = (
            (points.iloc[:, 0] == bot_conf[0]) &
            (points.iloc[:, 1] == bot_conf[1]) &
            (points.iloc[:, 2] == bot_conf[2]) &
            (points.iloc[:, 3] == bot_conf[3]) &
            (points.iloc[:, 4] == bot_conf[4])
    )
    matched_bot_points = points[condition_bot]
    condition_top = (
        (points.iloc[:, 0] == top_conf[0]) &
        (points.iloc[:, 1] == top_conf[1]) &
        (points.iloc[:, 2] == top_conf[2]) &
        (points.iloc[:, 3] == top_conf[3]) &
        (points.iloc[:, 4] == top_conf[4])
    )
    matched_top_points = points[condition_top]

    if matched_bot_points.shape[0] > 1:
        # print("more than one bot found")
        # one_matched_bot = matched_bottom_points.groupby(matched_bottom_points.columns[0, 1, 2, 3, 4]).columns[5].mean().reset_index()
        average_time = matched_bot_points[matched_bot_points.columns[5]].mean()
        matched_bot_points = matched_bot_points.iloc[[0]]
        matched_bot_points[matched_bot_points.columns[5]] = average_time
        assert matched_bot_points.shape[0] == 1, "There is bug in averaging bottom matches."
    if matched_top_points.shape[0] > 1:
        # print("more than one top found")
        # one_matched_top = matched_top_points.groupby(matched_top_points.columns[0, 1, 2, 3, 4]).columns[5].mean().reset_index()
        average_time = matched_top_points[matched_top_points.columns[5]].mean()
        matched_top_points = matched_top_points.iloc[[0]]
        matched_top_points[matched_top_points.columns[5]] = average_time
        assert matched_top_points.shape[0] == 1, "There is bug in averaging top matches."
    
    if pivot[5] > 1e+9: # if my time is invalid --> I am not local min
        invalid = 1
    elif matched_bot_points.empty and matched_top_points.empty: # if both my neighbours don't exist and my time is valid --> I am local min
        localmin = 1
        neighbours_invalid = 1
    elif matched_bot_points.empty: 
        top_time = matched_top_points[matched_top_points.columns[5]].iloc[0]
        if top_time > 1e+9 or top_time > pivot[5]: # if bot doesn't exist and top is worse --> I am local min
            localmin = 1
    elif matched_top_points.empty:
        bot_time = matched_bot_points[matched_bot_points.columns[5]].iloc[0]
        if bot_time > 1e+9 or bot_time > pivot[5]: # if top doesn't exist and bot is worse --> I am local min
            localmin = 1
    else:
        bot_time = matched_bot_points[matched_bot_points.columns[5]].iloc[0]
        top_time = matched_top_points[matched_top_points.columns[5]].iloc[0]
        if (bot_time > 1e+9) and (top_time > 1e+9): # if my time is valid and both neighbors' time is invalid --> I am local min
            localmin = 1
            neighbours_invalid = 1
        else:
            bot_is_worse = bot_time > pivot[5]
            top_is_worse = top_time > pivot[5]
            if bot_is_worse and top_is_worse: # if both neighbors have worse time than me --> I am local min
                localmin = 1
    return localmin, invalid, neighbours_invalid
