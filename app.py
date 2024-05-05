import streamlit as st
import pandas as pd
import requests
import pydeck as pdk
import math

st.set_page_config(page_title="World Crypto Forum", page_icon="app/static/logowhite.png", layout="centered", initial_sidebar_state="auto", menu_items=None)

conn = st.connection("postgresql", type="sql")
resources_df = conn.query('SELECT * FROM "Resource";', ttl="10m")
countries_df = conn.query('SELECT * FROM "Country";', ttl="10m")

st.image("static/logowhite.png", width = 200)
st.title("World Crypto Forum")

st.header("Country Leaderboard")
countries_df.sort_values(by='marketCap', ascending=False, inplace=True)
countries_df.reset_index(drop=True, inplace=True)
countries_df.index += 1
countries_leaderboard_df = countries_df.drop(columns=['id', 'createdAt', 'updatedAt', 'latitude', 'longitude'])
countries_leaderboard_df['abbrev'] = countries_leaderboard_df['abbrev'].str.upper()
#countries_leaderboard_df['marketCap'] = countries_leaderboard_df['marketCap'].apply(lambda x: f"${x:,.0f}")

countries_leaderboard_df['flag'] = countries_leaderboard_df['abbrev'].apply(lambda x: f'app/static/flags/{x}.png')
countries_leaderboard_df = countries_leaderboard_df.rename(columns={'flag': 'Flag', 'name': 'Country', 'marketCap': 'Market Cap'})
def format_market_cap(x):
    return '$ {:,.2f}'.format(x)
countries_leaderboard_df = countries_leaderboard_df.style.format({'Market Cap': format_market_cap})
st.dataframe(
    countries_leaderboard_df,
    column_config={
        "Flag": st.column_config.ImageColumn(),
        #"Market Cap": st.column_config.NumberColumn(format="$ %.2f")
    },
    column_order=["Flag", "Country", "Market Cap"],
)

m = 10000
n = 10000000
min_value = countries_df['marketCap'].min()
max_value = countries_df['marketCap'].max()

countries_df['normMarketCap'] = (((countries_df['marketCap'] - min_value) / (max_value - min_value)) * (n - m)) + m
countries_df['normMarketCap'] = countries_df['normMarketCap'].astype(int)
#countries_df['normMarketCap'] = (countries_df['marketCap'] - countries_df['marketCap'].mean()) / countries_df['marketCap'].std() * 100
#countries_df['normMarketCap'] = countries_df['normMarketCap'].astype(countries_df['marketCap'].dtype)
print(countries_df)
print(countries_df.dtypes)
#countries_df['normMarketCap'] = countries_df["marketCap"].apply(lambda exits_count: math.sqrt(exits_count))
#st.map(countries_df, size="normMarketCap")

st.header("Map")
st.pydeck_chart(pdk.Deck(
    map_style=None,
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=countries_df,
            pickable=True,
            opacity=0.3,
            stroked=True,
            filled=True,
            radius_scale=10,
            radius_min_pixels=40,
            radius_max_pixels=100,
            line_width_min_pixels=1,
            get_position='[longitude, latitude]',
            get_radius='normMarketCap',
            get_fill_color=[255, 140, 0],
            get_line_color=[0, 0, 0],
        ),
    ],
))