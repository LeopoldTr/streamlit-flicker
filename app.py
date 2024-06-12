import streamlit as st
import requests
from datetime import datetime


URL = "https://the-flicker2-wyqfoj2l7a-ew.a.run.app/"

# Page configuration
st.set_page_config(page_title="Movie Recommendations", page_icon=":clapper:", layout="wide")

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
        text-decoration: underline;
    }
    .rating {
        display: flex;
        align-items: center;
        font-size: 1.5em;
        color: gold;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .rating-text {
        margin-left: 5px;
        color: #e0e0e0;
    }
    .votes {
        font-size: 1em;
        color: #e0e0e0;
        margin-left: 10px;
    }
    .date {
        display: flex;
        align-items: center;
        font-size: 1.2em;
        color: #e0e0e0;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .date-icon {
        margin-right: 5px;
        color: #4CAF50;
    }
    .footer {
        position: fixed;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
        color: red;
        font-family: monospace;
        font-size: 0.8em;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title">Movie Recommendations</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Options")
st.sidebar.write("Use the options below to customize your searches.")
search_option = st.sidebar.radio("Search Type:", ("Rating Prediction", "Movie Recommendation"))

def display_rating(rating, votes):
    return f"""
    <div class="rating">
        ★
        <div class="rating-text">{rating}</div>
        <div class="votes">({votes} votes)</div>
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

if search_option == "Rating Prediction":
    st.markdown('<div class="header">Movie Rating Prediction</div>', unsafe_allow_html=True)
    movie_id = st.text_input("Enter the IMDB movie ID", placeholder="e.g., tt0089881")
    if movie_id:
        with st.spinner("Loading..."):
            response = requests.get(f"{URL}movie/{movie_id}/prediction")
            if response.status_code == 200:
                rating = response.json()
                st.write(f"Predicted rating: {rating}")
                st.markdown(display_rating(rating, 0), unsafe_allow_html=True)  # No votes in this case
            else:
                st.write('<div class="error">Error retrieving the prediction.</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="header">Movie Recommendations</div>', unsafe_allow_html=True)
    query = st.text_input("Enter keywords for recommendation", placeholder="e.g., harry magic snake school castle")
    if query:
        with st.spinner("Loading..."):
            response = requests.get(f"{URL}recommendation/?query={query}")
            if response.status_code == 200:
                recommendations = response.json()
                for rec in recommendations:
                    with st.expander(rec["Top Five Recommended Movies"]):
                        imdb_link = f"https://www.imdb.com/title/{rec['imdb_id']}/"
                        st.markdown(f"[View on IMDB]({imdb_link})")

                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**Rating:**")
                            st.markdown(display_rating(rec['Rating'], rec['numVotes']), unsafe_allow_html=True)
                            st.write(f"**Overview:** {rec['detail']['overview']}")
                            genres = ', '.join([genre['name'] for genre in rec['detail']['genres']])
                            st.write(f"**Genres:** {genres}")
                            st.markdown(display_date(rec['detail']['release_date']), unsafe_allow_html=True)
                        with col2:
                            st.image(f"https://image.tmdb.org/t/p/w500{rec['detail']['poster_path']}", width=150)
            else:
                st.write('<div class="error">Error retrieving the recommendations.</div>', unsafe_allow_html=True)

# Footer with fake security vulnerability link
st.markdown("""
    <div class="footer">
        <a href="https://t.ly/nGc_M" target="_blank">$ENV_VARIABLES</a>
    </div>
    """, unsafe_allow_html=True)
