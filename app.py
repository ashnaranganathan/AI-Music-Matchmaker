import os
import requests
from google import genai
import streamlit as st

st.set_page_config(
    page_title="AI Music Matchmaker", 
    page_icon="☁️", 
    layout="centered"
)

# Initialize Session State for Theme and History
if "theme" not in st.session_state:
    st.session_state.theme = "cloud_pastel"
if "history" not in st.session_state:
    st.session_state.history = []

# Theme Configurations
if st.session_state.theme == "cloud_pastel":
    bg_style = "linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 35%, #e0c3fc 70%, #8ec5fc 100%);"
    text_color = "#2D3748"
    input_bg = "rgba(255, 255, 255, 0.85)"
    btn_bg = "linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)"
    btn_text = "#2D3748"
else: # Dark Cyber Mode
    bg_style = "linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);"
    text_color = "#F1F5F9"
    input_bg = "rgba(30, 41, 59, 0.85)"
    btn_bg = "linear-gradient(135deg, #818cf8 0%, #c084fc 100%)"
    btn_text = "#FFFFFF"

st.markdown(f"""
    <style>
    .stApp {{
        background: {bg_style};
        background-attachment: fixed;
        color: {text_color};
    }}
    
    h1, h2, h3, h4, h5, h6, p, label {{
        color: {text_color} !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    .stTextInput input, .stTextArea textarea {{
        background-color: {input_bg} !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 12px !important;
        color: {text_color} !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }}

    div.stButton > button:first-child {{
        background: {btn_bg};
        color: {btn_text};
        border: none;
        border-radius: 25px;
        font-weight: 700;
        padding: 0.75rem 2rem;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease;
        width: 100%;
    }}
    
    div.stButton > button:first-child:hover {{
        transform: translateY(-2px);
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.25);
    }}

    /* Animated Wave Keyframes */
    @keyframes wave {{
        0%, 100% {{ height: 10px; }}
        50% {{ height: 40px; }}
    }}
    .wave-bar {{
        display: inline-block;
        width: 6px;
        height: 10px;
        margin: 0 2px;
        background-color: #8ec5fc;
        border-radius: 3px;
        animation: wave 1.2s infinite ease-in-out;
    }}
    .wave-bar:nth-child(2) {{ animation-delay: 0.1s; }}
    .wave-bar:nth-child(3) {{ animation-delay: 0.2s; }}
    .wave-bar:nth-child(4) {{ animation-delay: 0.3s; }}
    .wave-bar:nth-child(5) {{ animation-delay: 0.4s; }}
    </style>
""", unsafe_allow_html=True)

# Top Bar with Theme Toggle
top_col1, top_col2 = st.columns([4, 1])
with top_col1:
    st.title("☁️ AI Music Matchmaker")
with top_col2:
    if st.button("🌓 Toggle Theme"):
        st.session_state.theme = "dark_cyber" if st.session_state.theme == "cloud_pastel" else "cloud_pastel"
        st.rerun()

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
    try:
        response = requests.get(url, params=params).json()
        track = response["results"]["trackmatches"]["track"][0]
        return {
            "title": track["name"],
            "artist": track["artist"],
            "url": track["url"]
        }
    except (KeyError, IndexError, requests.RequestException):
        return None

# Input Section
st.subheader("1. Reference Track")
col1, col2 = st.columns(2)
with col1:
    song_input = st.text_input("Song Title", value="The Walls")
with col2:
    artist_input = st.text_input("Artist Name", value="Chase Atlantic")

st.subheader("2. What do you like about it?")

vibe_presets = [
    "🎸 Atmospheric Guitar Intro", 
    "🥁 Dark Trap Beat", 
    "🎤 Smooth Vocal Flow", 
    "🌌 Melancholic Lore", 
    "⚡ High Energy Entrance"
]
selected_vibe = st.pills("Quick Vibe Select:", vibe_presets, selection_mode="single")

# Interactive Audio Feature Filters
st.write("**Fine-tune parameters:**")
fcol1, fcol2, fcol3 = st.columns(3)
with fcol1:
    tempo_filter = st.select_slider("Tempo", options=["Chill / Slow", "Moderate", "Fast / Energetic"], value="Moderate")
with fcol2:
    mood_filter = st.select_slider("Mood", options=["Melancholic", "Balanced", "Upbeat"], value="Balanced")
with fcol3:
    era_filter = st.selectbox("Era Preference", ["Any Era", "Modern (2020s)", "2010s Hits", "Classic / Retro"])

initial_value = "Atmospheric guitar intro, dark beat, and smooth vocal flow"
if selected_vibe:
    initial_value = selected_vibe

elements_input = st.text_area(
    "Attributes or custom description:",
    value=initial_value,
    height=80
)

if st.button("✨ Find Matches", type="primary"):
    if not song_input.strip():
        st.warning("Please enter a song title!")
    else:
        # Custom Pastel Wave Animation Placeholder
        anim_placeholder = st.empty()
        anim_placeholder.markdown("""
            <div style="text-align: center; padding: 20px;">
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <p style="margin-top: 10px; font-weight: 600;">Analyzing musical elements & querying Gemini...</p>
            </div>
        """, unsafe_allow_html=True)
        
        track_data = search_lastfm_track(song_input, artist_input)
        
        if not track_data:
            anim_placeholder.empty()
            st.error("Song not found. Check the title or artist name.")
        else:
            prompt = f"""
            A listener likes the song '{track_data['title']}' by {track_data['artist']}.
            They enjoy these elements: "{elements_input}".
            
            Additional constraints:
            - Tempo: {tempo_filter}
            - Mood: {mood_filter}
            - Preferred Era: {era_filter}
            
            Recommend 4 real songs matching these musical traits.
            
            Format each song in clean Markdown:
            ### 🎵 [Song Title] - [Artist]
            * **Why it matches:** [1-2 sentence explanation focusing on requested features]
            * 🎧 **Listen:** [Spotify Search](https://open.spotify.com/search/[Song Title] [Artist]) | [YouTube Search](https://www.youtube.com/results?search_query=[Song Title]+[Artist])
            """
            
            response = gemini_client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )
            
            anim_placeholder.empty()
            
            # Store in Session State History
            st.session_state.history.append({
                "song": f"{track_data['title']} by {track_data['artist']}",
                "recommendations": response.text
            })
            
            st.success(f"Found reference track: **{track_data['title']}** by **{track_data['artist']}**")
            st.markdown("---")
            st.subheader("🎯 Recommended Songs")
            st.markdown(response.text)

# Search History Expander
if st.session_state.history:
    st.markdown("---")
    with st.expander("📜 Recent Search History"):
        for item in reversed(st.session_state.history[-5:]):
            st.markdown(f"**Reference:** {item['song']}")
            st.markdown(item['recommendations'])
            st.markdown("---")
