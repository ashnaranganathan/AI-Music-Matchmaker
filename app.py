import os
import requests
from google import genai
import streamlit as st

st.set_page_config(
    page_title="AI Music Matchmaker", 
    page_icon="☁️", 
    layout="centered"
)

# Custom CSS for Cloud Pastel Aesthetic
st.markdown("""
    <style>
    /* Cloud Pastel Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 35%, #e0c3fc 70%, #8ec5fc 100%);
        background-attachment: fixed;
        color: #2D3748;
    }
    
    /* Global Typography */
    h1, h2, h3, h4, h5, h6, p, label {
        color: #2D3748 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Soft Floating Card Container */
    [data-testid="stVerticalBlock"] > div {
        border-radius: 20px;
    }
    
    /* Input Fields Styling */
    .stTextInput input, .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.6) !important;
        border-radius: 12px !important;
        color: #2D3748 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #b8c6db !important;
        box-shadow: 0 0 10px rgba(161, 196, 253, 0.5) !important;
    }

    /* Soft Pastel Primary Button */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
        color: #2D3748;
        border: none;
        border-radius: 25px;
        font-weight: 700;
        padding: 0.75rem 2rem;
        box-shadow: 0 8px 20px rgba(142, 197, 252, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 25px rgba(142, 197, 252, 0.6);
        color: #1A202C;
    }
    </style>
""", unsafe_allow_html=True)

st.title("☁️ AI Music Matchmaker")
st.write("Find new songs based on specific elements like guitar intros, beats, or vocals.")

lastfm_key = os.environ.get("LASTFM_API_KEY")
gemini_key = os.environ.get("GEMINI_API_KEY")

if not (lastfm_key and gemini_key):
    st.error("⚠️ Missing API keys! Ensure LASTFM_API_KEY and GEMINI_API_KEY are exported in your terminal.")
    st.stop()

gemini_client = genai.Client(api_key=gemini_key)

def search_lastfm_track(song_title, artist_name=""):
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "track.search",
        "track": song_title,
        "artist": artist_name,
        "api_key": lastfm_key,
        "format": "json",
        "limit": 1
    }
    response = requests.get(url, params=params).json()
    try:
        track = response["results"]["trackmatches"]["track"][0]
        return {
            "title": track["name"],
            "artist": track["artist"],
            "url": track["url"]
        }
    except (KeyError, IndexError):
        return None

# Input Section
st.subheader("1. Reference Track")
col1, col2 = st.columns(2)
with col1:
    song_input = st.text_input("Song Title", value="The Walls")
with col2:
    artist_input = st.text_input("Artist Name", value="Chase Atlantic")

st.subheader("2. What do you like about it?")
elements_input = st.text_area(
    "Attributes (e.g. guitar intro, vocal style, dark beat, bass, mood):",
    value="Atmospheric guitar intro, dark beat, and smooth vocal flow",
    height=100
)

if st.button("✨ Find Matches", type="primary"):
    if not song_input.strip():
        st.warning("Please enter a song title!")
    else:
        with st.spinner("Searching Last.fm music database..."):
            track_data = search_lastfm_track(song_input, artist_input)
            
            if not track_data:
                st.error("Song not found. Check the title or artist name.")
            else:
                st.success(f"Found: **{track_data['title']}** by **{track_data['artist']}**")
                
                with st.spinner("Generating matches with Gemini..."):
                    prompt = f"""
                    A listener likes the song '{track_data['title']}' by {track_data['artist']}.
                    They specifically enjoy these elements: "{elements_input}".
                    
                    Recommend 4 real songs that match these specific musical qualities.
                    
                    Format response in clean Markdown:
                    ### 🎵 [Song Title] - [Artist]
                    * **Why it matches:** [1-2 sentence explanation focusing on requested features]
                    * **Listen:** [Search on Spotify](https://open.spotify.com/search/[Song Title] [Artist])
                    """
                    
                    response = gemini_client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt
                    )
                    
                    st.markdown("---")
                    st.subheader("🎯 Recommended Songs")
                    st.markdown(response.text)
