import streamlit as st
from googleapiclient.discovery import build

API_KEY = 'AIzaSyC7JQbgRAv4YjHkSThBtzcY31ij0udFwsQ'
youtube = build('youtube', 'v3', developerKey=API_KEY)

channelId = "UCsVz2qkd_oGXGC66fcH4SFA"

next_page_token = None

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
        
# Start of front end display
st.title("League VOD Manager")


champion = st.text_input("Enter a champion:")

if champion:
    for key in get_channel_playlists(channelId):
        if champion in key:
            id = get_channel_playlists(channelId).get(key)
            st.write(f"{champion} playlist found!")
            for key in get_videos(id):
                st.button(key) # fetch videos of title playlist
            break
    st.write(f"{champion} playlist not found...")

