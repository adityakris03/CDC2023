from requests import post, get
from dotenv import load_dotenv
import os
from json import dump
from tqdm import tqdm
import time
load_dotenv()
# Get access token if needed
# url = 'https://accounts.spotify.com/api/token'
# headers = {'Content-Type': 'application/x-www-form-urlencoded'}
# body = {'grant_type': 'client_credentials', 'client_id': os.getenv("CLIENT_ID"), 'client_secret': os.getenv("CLIENT_SECRET")}
# res = post(url, headers=headers, data=body)
# print(res.json())

base_url = 'https://api.spotify.com/v1/'
headers = {'Authorization': 'Bearer BQAoSJTDoSUe2c7IMD-IQ9hJhW4-3wkYxWjbbkO-MmIitVIy7pamEH34xW5c0ZUmPp_8Cf2tkPqXZHWvX9T44C48vgh-15onTpVsZT33bdKChkGD36I'}
def search(query):
    tracks = {}
    for i in range(0, 1000, 50):
        query_param = {'q': query, 'type': ['track'], 'limit': 50, 'offset': i}
        res = get(base_url + 'search', headers=headers, params=query_param)
        print(res.status_code)
        audio_features = get(base_url + 'audio-features/', headers=headers, params={'ids': ','.join([track['id'] for track in res.json()['tracks']['items']])})
        print(audio_features.status_code)
        for track, audio_f in tqdm(zip(res.json()['tracks']['items'], audio_features.json()['audio_features'])):
            tracks[track['id']] = {'popularity': track['popularity'], 'danceability': audio_f['danceability'], 'energy': audio_f['energy'], 'key': audio_f['key'], 'loudness': audio_f['loudness'], 'mode': audio_f['mode'], 'speechiness': audio_f['speechiness'], 'acousticness': audio_f['acousticness'], 'instrumentalness': audio_f['instrumentalness'], 'liveness': audio_f['liveness'], 'valence': audio_f['valence'], 'tempo': audio_f['tempo'], 'duration_ms': audio_f['duration_ms'], 'time_signature': audio_f['time_signature'], 'genre': [artist['genres'] for artist in track['artists']]}
        time.sleep(3)
    return tracks


for year in range(2001, 2011):
    tracks = search(f'year:{year}')
    with open(f'{year}.json', 'w') as f:
        dump(tracks, f)