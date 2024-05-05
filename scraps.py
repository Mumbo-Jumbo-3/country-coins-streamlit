'''
m = 0
n = 100
min_value = countries_df['marketCap'].min()
max_value = countries_df['marketCap'].max()
countries_leaderboard_df['progress'] = (((countries_df['marketCap'] - min_value) / (max_value - min_value)) * (n - m)) + m
'''