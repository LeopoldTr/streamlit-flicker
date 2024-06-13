import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
from streamlit_searchbox import st_searchbox

URL = "https://the-flicker4-wyqfoj2l7a-ew.a.run.app/"

# Page configuration
st.set_page_config(page_title="The Flicker", page_icon=":clapper:", layout="wide")

# Custom CSS for appearance improvement
st.markdown("""
    <style>
    .main {
        background-color: #1e1e1e;
        color: #e0e0e0;
        font-family: Arial, sans-serif;
    }
    .title {
        font-size: 2.5em;
        background: -webkit-linear-gradient(left, #FF4B4B, #FFC837);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 20px;
    }
    .header {
        font-size: 2em;
        color: #e0e0e0;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .subheader {
        font-size: 1.5em;
        color: #e0e0e0;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .card {
        background-color: #333333;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }
    .error {
        color: red;
    }
    a {
        color: #4CAF50;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline.
    }
    .rating {
        display: flex;
        align-items: center;
        font-size: 1.5em;
        color: gold;
        margin-top: 10px;
        margin-bottom: 10px.
    }
    .rating-text {
        margin-left: 5px.
        color: #e0e0e0.
    }
    .votes {
        font-size: 1em.
        color: #e0e0e0.
        margin-left: 10px.
    }
    .date {
        display: flex.
        align-items: center.
        font-size: 1.2em.
        color: #e0e0e0.
        margin-top: 10px.
        margin-bottom: 10px.
    }
    .date-icon {
        margin-right: 5px.
        color: #4CAF50.
    }
    .footer {
        position: fixed.
        bottom: 10px.
        left: 50%.
        transform: translateX(-50%).
        color: red.
        font-family: monospace.
        font-size: 0.8em.
    }
    </style>
    """, unsafe_allow_html=True)

# Display the custom logo using matplotlib
st.markdown('<div class="title">The Flicker</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Options")
st.sidebar.write("Use the options below to customize your searches.")
search_option = st.sidebar.radio("Search Type:", ("Rating Prediction", "Movie Recommendation"))

def display_rating(rating, votes=None):
    votes_html = f'<div class="votes">({votes} votes)</div>' if votes is not None else ''
    return f"""
    <div class="rating">
        ★
        <div class="rating-text">{rating}</div>
        {votes_html}
    </div>
    """

def display_date(date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d')
    formatted_date = date.strftime('%d %B %Y')
    return f"""
    <div class="date">
        <span class="date-icon">📅</span>
        <span>{formatted_date}</span>
    </div>
    """

def sentimental_analysis_plot(sentiment_dict, title):
    sentiments = ['surprise', 'anger', 'joy', 'fear', 'sadness', 'love']
    values = [sentiment_dict[sentiment] for sentiment in sentiments]
    result_percentage = ["%.0f%%" % (100 * res) for res in values]
    columns = [word.upper() for word in sentiments]

    df = pd.DataFrame({'SENTIMENT': columns, 'VALUE': values, 'PERCENTAGE': result_percentage})
    df = df.sort_values(by='VALUE',ascending=True).reset_index(drop=True)
    max_value_full_ring = max(df['VALUE'])

    ring_colours = ['#665191', '#a05195', '#d45087', '#f95d6a', '#ff7c43', '#ffa600']
    ring_labels = [f'   {x} ({v}) ' for x, v in zip(list(df['SENTIMENT']), list(df['PERCENTAGE']))]
    data_len = len(df)

    fig = plt.figure(figsize=(5, 5), linewidth=10, edgecolor='#393d5c', facecolor='#000000')
    fig.suptitle(f"SENTIMENT ANALYSIS FOR '{title.upper()}'", fontsize=10, fontweight='bold', color='white')

    rect = [0.1, 0.1, 0.8, 0.8]

    ax_polar_bg = fig.add_axes(rect, polar=True, frameon=False)
    ax_polar_bg.set_theta_zero_location('N')
    ax_polar_bg.set_theta_direction(1)

    for i in range(data_len):
        ax_polar_bg.barh(i, max_value_full_ring * 1.5 * np.pi / max_value_full_ring, color='black', alpha=0.1)
    ax_polar_bg.axis('off')

    ax_polar = fig.add_axes(rect, polar=True, frameon=False)
    ax_polar.set_theta_zero_location('N')
    ax_polar.set_theta_direction(1)
    ax_polar.set_rgrids([0, 1, 2, 3, 4, 5], labels=ring_labels, angle=0, fontsize=7, fontweight='bold', color='white', verticalalignment='center')

    for i in range(data_len):
        ax_polar.barh(i, list(df['VALUE'])[i] * 1.5 * np.pi / max_value_full_ring, color=ring_colours[i])

    return fig

# Function to search movies
def search_movies(query):
    response = requests.get(f"{URL}search/", params={"query": query})
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Page for Rating Prediction
if search_option == "Rating Prediction":
    st.markdown('<div class="header">Movie Rating Prediction</div>', unsafe_allow_html=True)

    # Using streamlit-searchbox
    selected_movie = st_searchbox(
        search_movies,
        key="searchbox_movie",
        placeholder="Enter the movie name",
    )
    print(f"Search Movie :: {selected_movie}")
    if selected_movie:
        selected_movie_id = selected_movie['id_imdb']
        with st.spinner("Loading..."):
            response = requests.get(f"{URL}movie/{selected_movie_id}/prediction")
            if response.status_code == 200:
                data = response.json()
                rec = data[0] if isinstance(data, list) else data

                imdb_link = f"https://www.imdb.com/title/{rec['movie_details']['imdb_id']}/"
                st.markdown(f"[View on IMDB]({imdb_link})")

                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Predicted Rating:**")
                    st.markdown(display_rating(round(rec['prediction'])), unsafe_allow_html=True)
                    st.write(f"**Actual Rating:**")
                    st.markdown(display_rating(rec['movie_details']['vote_average'], rec['movie_details']['vote_count']), unsafe_allow_html=True)
                    st.write(f"**Overview:** {rec['movie_details']['overview']}")
                    genres = ', '.join([genre['name'] for genre in rec['movie_details']['genres']])
                    st.write(f"**Genres:** {genres}")
                    st.markdown(display_date(rec['movie_details']['release_date']), unsafe_allow_html=True)
                with col2:
                    st.image(f"https://image.tmdb.org/t/p/w500{rec['movie_details']['poster_path']}", width=150)

                # Plot sentimental analysis
                col1,col2, col3 = st.columns([1, 1, 1])
                with col2:
                    sentiment_fig = sentimental_analysis_plot(rec['sentiment_dict'][0], rec['movie_details']['title'])
                    st.pyplot(sentiment_fig)
            else:
                st.write('<div class="error">Error retrieving the prediction.</div>', unsafe_allow_html=True)

# Page for Movie Recommendations
else:
    st.markdown('<div class="header">Movie Recommendations</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])

    with col1:
        query = st.text_input("Enter keywords for recommendation", placeholder="e.g., harry magic snake school castle")

    with col2:
        sort_option = st.selectbox("Sort By:", ["order", "rank", "popular"])

    if query:
        with st.spinner("Loading..."):
            response = requests.get(f"{URL}recommendation/?query={query}&sort={sort_option}")
            if response.status_code == 200:
                recommendations = response.json()
                for rec in recommendations:
                    imdb_link = f"https://www.imdb.com/title/{rec['imdb_id']}/"
                    st.markdown(f"[View on IMDB]({imdb_link})")

                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**Rating:**")
                        st.markdown(display_rating(rec['averageRating'], rec['numVotes']), unsafe_allow_html=True)
                        st.write(f"**Overview:** {rec['detail']['overview']}")
                        genres = ', '.join([genre['name'] for genre in rec['detail']['genres']])
                        st.write(f"**Genres:** {genres}")
                        st.markdown(display_date(rec['detail']['release_date']), unsafe_allow_html=True)
                    with col2:
                        st.image(f"https://image.tmdb.org/t/p/w500{rec['detail']['poster_path']}", width=150)
            else:
                st.write('<div class="error">Error retrieving the recommendations.</div>', unsafe_allow_html=True)
