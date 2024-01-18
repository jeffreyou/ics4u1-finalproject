import streamlit as st
from googleapiclient.discovery import build

API_KEY = 'AIzaSyC7JQbgRAv4YjHkSThBtzcY31ij0udFwsQ'
youtube = build('youtube', 'v3', developerKey=API_KEY)

channelId = "UCsVz2qkd_oGXGC66fcH4SFA"

next_page_token = None
runs = 0
results = 0
queries = 0
champions = (
    "All Results","Aatrox","Ahri","Akali","Akshan","Alistar","Amumu","Anivia","Annie","Aphelios","Ashe","Aurelion Sol","Azir","Bard","Bel'Veth","Blitzcrank","Brand",
    "Braum","Briar","Caitlyn","Camille","Cassiopeia","Cho'Gath","Corki","Darius","Diana","Dr. Mundo","Draven","Ekko","Elise","Evelynn","Ezreal","Fiddlesticks",
    "Fiora","Fizz","Galio","Gangplank","Garen","Gnar","Gragas","Graves","Gwen","Hecarim","Heimerdinger","Hwei","Illaoi","Irelia","Ivern","Janna","Jarvan IV","Jax",
    "Jayce","Jhin","Jinx","K'Sante","Kai'Sa","Kalista","Karma","Karthus","Kassadin","Katarina","Kayle","Kayn","Kennen","Kha'Zix","Kindred","Kled","Kog'Maw","Leblanc",
    "Lee Sin","Leona","Lillia","Lissandra","Lucian","Lulu","Lux","Malphite","Malzahar","Maokai","Master Yi","Milio","Miss Fortune","Mordekaiser","Morgana","Naafiri",
    "Nami","Nasus","Nautilius","Neeko","Nidalee","Nilah","Nocturne","Nunu & Willump","Olaf","Orianna","Ornn","Pantheon","Poppy","Pyke","Qiyana","Quinn","Rakan","Rammus",
    "Rek'Sai","Rell","Renata Glasc","Renekton","Rengar","Riven","Rumble","Ryze","Samira","Sejuani","Senna","Seraphine","Sett","Shaco","Shen","Shyvana","Singed","Sion",
    "Sivir","Skarner","Sona","Soraka","Swain","Sylas","Syndra","Tahm Kench","Taliyah","Talon","Taric","Teemo","Thresh","Tristana","Trundle","Tryndamere","Twisted Fate",
    "Twitch","Udyr","Urgot","Varus","Vayne","Veigar","Vel'Koz","Vex","Vi","Viego","Viktor","Vladimir","Volibear","Warwick","Wukong","Xayah","Xerath","Xin Zhao","Yasuo",
    "Yone","Yorick","Yuumi","Zac","Zed","Zeri","Ziggs","Zilean","Zoe","Zyra"
)
roles = (
    "All Results","Top","Jungle","Mid","Bottom","Support"
)

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
    global queries

    id = get_channel_playlists(channelId).get(key)
    total = len(get_videos(id))
    progress_text = f"Searching {champion} ({results} / {total})..."
    progress_bar = st.progress(0, text=progress_text)
    for key in get_videos(id):
        if opponent in key and any(r in key for r in role):
            if queries < max_queries:
                queries += 1
                st.link_button(key,f'https://www.youtube.com/watch?v={get_videos(id)[key]}') # creates button that passes title and videoId
        results += 1
        progress_bar.progress(results / total, text=f"Searching {champion} ({results} / {total})...")

# Start of front end display
st.title("League VOD Manager")
st.divider()
st.caption('_Find High Elo Gameplay with :red[Ease]_')


champion = st.selectbox("**Enter a champion:**", champions)

role = st.selectbox('**Choose Role:**', roles)
if role == "All Results":
    role = "Patch" # all titles contain 'Patch'
elif role == "Bottom":
    role = ["Carry","ADC"]

opponent = st.selectbox('**Choose Matchup:**', champions)
if opponent == "All Results":
    opponent = 'vs' # all titles contain 'vs'

max_queries = st.slider("Select max video results: ",max_value=50)

submit = st.button("Search")
st.divider()

if submit: # change to if submit button is pressed
    runs += 1
    if runs == 2:
        st.rerun()
    with st.expander('**Video Results:**'):
        for key in get_channel_playlists(channelId):
            if champion == key.split(' ')[0]: # split string to isolate first word to avoid "viego" when searching "Vi" problem
                display_video(champion,key)

'''
things to add:
styling
error messages 
docstrings to functions 
'''