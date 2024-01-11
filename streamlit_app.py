import streamlit as st
from googleapiclient.discovery import build

API_KEY = 'AIzaSyC7JQbgRAv4YjHkSThBtzcY31ij0udFwsQ'
youtube = build('youtube', 'v3', developerKey=API_KEY)

channelId = "UCsVz2qkd_oGXGC66fcH4SFA"

next_page_token = None
runs = 0
results = 0

def get_playlist_info(channelId, page_token=None):
    global next_page_token
    request = youtube.playlists().list(
        part="snippet",
        channelId=channelId,
        maxResults=50,
        pageToken=page_token,
    )
    response = request.execute()
    return response

def get_channel_playlists(channelId):
    playlists = {} # dict of playlist titles and ids
    global next_page_token

    while True:
        # Request the playlists for the given channel
        response = get_playlist_info(channelId, page_token=next_page_token)

        # Extract playlist titles
        for playlist in response.get('items', []):
            playlists[playlist['snippet']['title']] = playlist['id'] # Assigns key of title, value of playlist id

        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            return playlists


def get_videos(id,page_token=None):
    videos = {} # dict of video titles and ids

    while True:
        request = youtube.playlistItems().list(
            part=["contentDetails","id","snippet","status"],
            playlistId = id,
            maxResults = 50,
            pageToken = page_token
        )
        response = request.execute()

        for playlistItems in response.get('items', []):
            videos[playlistItems['snippet']['title']] = playlistItems['contentDetails']['videoId']
        
        page_token = response.get('nextPageToken')

        if not page_token:
            return videos

def display_video(champion,key):
    global results
    id = get_channel_playlists(channelId).get(key)
    total = len(get_videos(id))
    progress_text = f"Searching {champion} ({results} / {total})..."
    progress_bar = st.progress(0, text=progress_text)
    for key in get_videos(id):
        st.link_button(key,f'https://www.youtube.com/watch?v={get_videos(id)[key]}') # creates button that passes title and videoId
        results += 1
        progress_bar.progress(results / total, text=f"Searching {champion} ({results} / {total})...")
    
# Start of front end display
st.title("League VOD Manager")


champion = st.text_input("Enter a champion:")

if champion:
    runs += 1
    if runs == 2:
        st.rerun()
    with st.expander(f'Videos'):
        for key in get_channel_playlists(channelId):
            if champion in key:
                display_video(champion,key)
                '''
                id = get_channel_playlists(channelId).get(key)
                total = len(get_videos(id))
                progress_text = f"Searching {champion} ({results} / {total})..."
                progress_bar = st.progress(0, text=progress_text)
                for key in get_videos(id):
                    st.link_button(key,f'https://www.youtube.com/watch?v={get_videos(id)[key]}') # creates button that passes title and videoId
                    results += 1
                    progress_bar.progress(results / total, text=f"Searching {champion} ({results} / {total})...")
                break
                '''

'''
things to add:
filters (role, matchup, size, patch?)
style the website to look better
add more functions to make code more readable 
'''