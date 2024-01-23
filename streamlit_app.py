import streamlit as st
from googleapiclient.discovery import build

API_KEY = 'AIzaSyC7JQbgRAv4YjHkSThBtzcY31ij0udFwsQ'
youtube = build('youtube', 'v3', developerKey=API_KEY)

channelId = "UCsVz2qkd_oGXGC66fcH4SFA"

next_page_token = None
runs = 0 # used to reset program when user presses "search" again
results = 0 # used to keep show realtime search progress
queries = 0 # used to identify how many results to output
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

roles = ("All Results","Top","Jungle","Mid","Bottom","Support")

def get_playlist_info(channelId, page_token=None):
    '''
    retrieves return data of playlist tab for specified channel

    args:
        channelId - string, identifies the channel to fetch data for
        page_token - string, used to identify the page number

    return:
        response - string, body of return data
    '''
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
    '''
    retrieves a dictionary of channel playlist titles and ids for specified channel

    args:
        channelId - string, identifies the channel to fetch data for
        
    return:
        playlists - dict, key is playlist name and value is playlist id
    '''
    playlists = {} # dict of playlist titles and ids
    global next_page_token

    while True:
        # Request the playlists for the given channel
        response = get_playlist_info(channelId, page_token=next_page_token)

        # Extract playlist titles
        for playlist in response.get('items', []):
            playlists[playlist['snippet']['title']] = playlist['id'] # Assigns key of title, value of playlist id

        next_page_token = response.get('nextPageToken')

        if not next_page_token: # checks if there are any more pages to fetch
            return playlists


def get_videos(id,page_token=None):
    '''
    retrieves a dictionary of playlist video titles and ids for specified channel

    args:
        id - string, identifies playlist to fetch data for
        page_token - string, used to identify the page number

    return:
        videos - dict, key is video name and value is video id
    '''
    videos = {} # dict of video titles and ids

    while True:
        request = youtube.playlistItems().list(
            part=["contentDetails","id","snippet","status"],
            playlistId = id,
            maxResults = 50,
            pageToken = page_token
        )
        response = request.execute()

        for playlistItems in response.get('items', []): # populates videos dict
            videos[playlistItems['snippet']['title']] = playlistItems['contentDetails']['videoId']
        
        page_token = response.get('nextPageToken')

        if not page_token: # checks if there are any more pages to fetch
            return videos

def display_video(champion,key):
    '''
    outputs button of corresponding video that leads to YouTube URL

    args:
        champion - string, name of queried champion
        key - string, name of playlist title
    '''
    global results
    global queries

    id = get_channel_playlists(channelId).get(key)
    total = len(get_videos(id))
    progress_text = f"Searching {champion} ({results} / {total})..."
    progress_bar = st.progress(0, text=progress_text)

    for key in get_videos(id): # iterates through each title in champion playlist
        if type(role) == str: 
            if opponent in key and role in key:
                if queries < max_queries:
                    queries += 1
                    st.link_button(key,f'https://www.youtube.com/watch?v={get_videos(id)[key]}') # creates button that passes title and videoId
        else: # used if selected role is bottom (ADC and Carry both correspond)
            if opponent in key and any(r in key for r in role):
                if queries < max_queries:
                    queries += 1
                    st.link_button(key,f'https://www.youtube.com/watch?v={get_videos(id)[key]}') # creates button that displays title and redirects to URL on click
        results += 1
        progress_bar.progress(results / total, text=f"Searching {champion} ({results} / {total})...") # updates progress bar through each iteration

# Start of front end display
st.title("League VOD Manager 📽️")
st.divider()
st.caption('_Find High Elo Gameplay with :red[Ease]_')

champion = st.selectbox("**Enter a champion:**", champions[1:], index=None, placeholder="Aatrox, Ahri, Akali...")

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

if submit: # if search button is pressed
    runs += 1
    if runs == 2: # resets program if search button is pressed again
        st.rerun()
    with st.expander('**Video Results:**'):
        for key in get_channel_playlists(channelId):
            if champion == key.split(' ')[0] or champion == key.split(' ')[0] + ' ' + key.split(' ')[1]: # split string to isolate first word to avoid "viego" when searching "Vi" problem, also allows 'aurelion sol' or 'lee sin' to be searched
                display_video(champion,key)