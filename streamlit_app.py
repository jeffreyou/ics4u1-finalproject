
''' 
def get_playlists():
    playlists = []
    index = 0
    playlist_request = youtube.playlists().list(
    part='snippet',
    channelId = 'UCsVz2qkd_oGXGC66fcH4SFA',
    maxResults = 100
    )
    playlist_response = playlist_request.execute()
    maxResults = 100
    while len(playlists) < maxResults: # Iterating through playlists page 
        playlists += playlist_response['items'][index]['snippet']['title']
        playlist_request = youtube.playlists().list_next(playlist_request, playlist_response)
        index += 1
    return playlists

st.write(get_playlists())
'''

#for title in playlist_response.playlists[snippet][title]:
   #  st.write(playlist_response.playlists[snippet][title])

import streamlit as st
from googleapiclient.discovery import build

API_KEY = 'AIzaSyC7JQbgRAv4YjHkSThBtzcY31ij0udFwsQ'
youtube = build('youtube', 'v3', developerKey=API_KEY)

channelId = "UCsVz2qkd_oGXGC66fcH4SFA"

next_page_token = None # Used to check page turns
def get_playlist_info(channelId):
    request = youtube.playlists().list( # States request parameters
    part="snippet",
    channelId=channelId,
    maxResults=50,
    pageToken = next_page_token,
    )
    response = request.execute()
    return response
    
def get_channel_playlists(channelId):
    playlists = []

    while True:
        # Request the playlists for the given channel
        get_playlist_info(channelId)
        next_page_token = get_playlist_info(channelId).get('nextPageToken')
        # Extract playlist titles
        for playlist in get_playlist_info(channelId).get('items', []):
            playlists.append(playlist['snippet']['title'])
        return playlists
       


st.title("League VOD Manager")

champion = st.text_input("Enter a champion:")
if champion:
    st.write(f"Searching for {champion}...")

'''
if champion: # Only starts once value is entered
    for title in get_channel_playlists(channelId):
        if champion in title:
            st.write(f"{champion} playlist found!")
'''
st.write(get_channel_playlists(channelId))


