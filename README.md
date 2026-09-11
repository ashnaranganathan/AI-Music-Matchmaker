#  AI Music Matchmaker

An AI-driven music recommendation web application built with **Streamlit**, **Last.fm API**, and **Google Gemini 3.6 Flash**. 

AI Music Matchmaker finds new music based on specific audio attributes, arrangement features, and moods—such as atmospheric guitar intros, dark trap beats, or smooth vocal flows—rather than relying solely on generic genre tags.

---

##  Key Features

* ** Cloud-Pastel & Cyber Dark UI:** Styled with custom CSS featuring soft pastel gradients, rounded card containers, and a one-click theme toggle switch.
* ** Last.fm Track Verification:** Queries the Last.fm database to verify reference tracks and retrieve accurate metadata.
* ** Gemini 3.6 Flash Intelligence:** Leverages Google's `gemini-3.6-flash` model to analyze track characteristics and recommend matching songs.
* ** Preset Vibe Pills & Audio Filters:** Quick-select preset tags (*Atmospheric Guitar Intro*, *Dark Trap Beat*, *Smooth Vocal Flow*) alongside fine-tuning sliders for tempo, mood, and release era.
* ** Direct Streaming Search Links:** Formats generated recommendations with direct search shortcuts for Spotify and YouTube.
* ** Session History:** Tracks your recent searches during your active session so you can compare previous recommendations.

---

##  Tech Stack

* **Frontend/Framework:** [Streamlit](https://streamlit.io/)
* **AI Model:** [Google Gemini API](https://ai.google.dev/) (`gemini-3.6-flash`) via the `google-genai` SDK
* **Music Data:** [Last.fm API](https://www.lastfm.api)
* **Environment & Language:** Python 3.13, macOS

---

##  Getting Started Locally

### Prerequisites

Ensure you have Python installed and request API keys for:
1. **Google Gemini API Key:** [Google AI Studio](https://aistudio.google.com/)
2. **Last.fm API Key:** [Last.fm API Accounts](https://www.lastfm.com/api/account/create)

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ashnaranganathan/AI-Music-Matchmaker.git](https://github.com/ashnaranganathan/AI-Music-Matchmaker.git)
   cd AI-Music-Matchmaker
