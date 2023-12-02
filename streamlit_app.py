import streamlit as st
<<<<<<< HEAD
import pytube
from pytube import Channel

st.title("League VOD Manager")

champion = st.text_input("Enter a champion:")
if champion:
    st.write(f"Searching for {champion}...")

c = Channel('https://www.youtube.com/c/ChallengerReplays/videos')
for url in c.video_urls:
    st.write(url, c.video_urls)
=======

st.title('Test')
champion = st.text_input("**Enter Champion:**")
>>>>>>> 1be65d6802b1b60c8ca9ca28754e1f33ec553536
