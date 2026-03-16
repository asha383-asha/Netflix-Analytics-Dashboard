import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# Page Setup
# ----------------------------

st.set_page_config(page_title="Netflix Analytics Dashboard", layout="wide")

st.title("🎬 Netflix Analytics Dashboard")

# ----------------------------
# Load Dataset
# ----------------------------

df = pd.read_csv("netflix_titles.csv")

# Cleaning
df['director'] = df['director'].fillna("Unknown")
df['cast'] = df['cast'].fillna("Unknown")
df['country'] = df['country'].fillna("Unknown")
df['rating'] = df['rating'].fillna("Unknown")

df['date_added'] = df['date_added'].str.strip()
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month

# ----------------------------
# Sidebar Filters
# ----------------------------

st.sidebar.header("Dashboard Filters")

type_filter = st.sidebar.multiselect(
    "Select Type",
    df['type'].unique(),
    default=df['type'].unique()
)

country_filter = st.sidebar.multiselect(
    "Select Country",
    df['country'].unique(),
    default=df['country'].unique()
)

year_filter = st.sidebar.multiselect(
    "Select Year",
    sorted(df['year_added'].dropna().unique()),
    default=sorted(df['year_added'].dropna().unique())
)

filtered_df = df[
    (df['type'].isin(type_filter)) &
    (df['country'].isin(country_filter)) &
    (df['year_added'].isin(year_filter))
]

# ----------------------------
# Search Movie Title
# ----------------------------

search_title = st.sidebar.text_input("Search Movie / Show")

if search_title:
    filtered_df = filtered_df[
        filtered_df['title'].str.contains(search_title, case=False)
    ]

# ----------------------------
# KPI Cards
# ----------------------------

total_titles = filtered_df.shape[0]
movies = filtered_df[filtered_df['type']=="Movie"].shape[0]
tv_shows = filtered_df[filtered_df['type']=="TV Show"].shape[0]
countries = filtered_df['country'].nunique()

col1,col2,col3,col4 = st.columns(4)

col1.metric("Total Titles", total_titles)
col2.metric("Movies", movies)
col3.metric("TV Shows", tv_shows)
col4.metric("Countries", countries)

# ----------------------------
# Row 1
# ----------------------------

col5,col6 = st.columns(2)

with col5:
    type_count = filtered_df['type'].value_counts()

    fig1 = px.pie(
        values=type_count.values,
        names=type_count.index,
        title="Movies vs TV Shows",
        color_discrete_sequence=['#E50914','#FFB6B6']
    )

    st.plotly_chart(fig1,use_container_width=True)

with col6:
    rating_data = filtered_df['rating'].value_counts().head(10)

    fig2 = px.bar(
        x=rating_data.index,
        y=rating_data.values,
        title="Ratings Distribution",
        color=rating_data.values,
        color_continuous_scale="Reds"
    )

    st.plotly_chart(fig2,use_container_width=True)

# ----------------------------
# Row 2
# ----------------------------

col7,col8 = st.columns(2)

with col7:
    genre_count = filtered_df['listed_in'].value_counts().head(10)

    fig3 = px.bar(
        x=genre_count.values,
        y=genre_count.index,
        orientation='h',
        title="Top Genres",
        color=genre_count.values,
        color_continuous_scale="Reds"
    )

    st.plotly_chart(fig3,use_container_width=True)

with col8:
    year_data = filtered_df['year_added'].value_counts().sort_index()

    fig4 = px.area(
        x=year_data.index,
        y=year_data.values,
        title="Content Added by Year"
    )

    st.plotly_chart(fig4,use_container_width=True)

# ----------------------------
# Row 3
# ----------------------------

col9,col10 = st.columns(2)

with col9:
    country_data = filtered_df['country'].value_counts().head(10)

    fig5 = px.bar(
        x=country_data.values,
        y=country_data.index,
        orientation='h',
        title="Top Countries Producing Content",
        color=country_data.values,
        color_continuous_scale="Reds"
    )

    st.plotly_chart(fig5,use_container_width=True)

with col10:
    month_data = filtered_df['month_added'].value_counts().sort_index()

    fig6 = px.line(
        x=month_data.index,
        y=month_data.values,
        title="Content Added by Month"
    )

    st.plotly_chart(fig6,use_container_width=True)

# ----------------------------
# Top Actors Analysis
# ----------------------------

st.subheader("⭐ Top Actors on Netflix")

actor_series = filtered_df['cast'].str.split(',').explode().value_counts().head(10)

fig7 = px.bar(
    x=actor_series.values,
    y=actor_series.index,
    orientation='h',
    title="Top Actors",
    color=actor_series.values,
    color_continuous_scale="Reds"
)

st.plotly_chart(fig7,use_container_width=True)

# ----------------------------
# Duration Analysis
# ----------------------------

st.subheader("🎥 Movie Duration Analysis")

movies_df = filtered_df[filtered_df['type']=="Movie"]

movies_df['duration'] = movies_df['duration'].str.replace(" min","")

movies_df['duration'] = pd.to_numeric(movies_df['duration'], errors='coerce')

fig8 = px.histogram(
    movies_df,
    x="duration",
    nbins=30,
    title="Movie Duration Distribution"
)

st.plotly_chart(fig8,use_container_width=True)

# ----------------------------
# World Map
# ----------------------------

st.subheader("🌍 Netflix Content by Country")

country_map = filtered_df['country'].value_counts().reset_index()
country_map.columns = ['country','count']

fig9 = px.choropleth(
    country_map,
    locations="country",
    locationmode="country names",
    color="count",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig9,use_container_width=True)