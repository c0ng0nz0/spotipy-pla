import json
import time

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

def get_track_ids(playlist_id):
	music_id_list = []
	playlist = spotify.playlist(playlist_id)
	for item in playlist['tracks']['items']:
		music_track = item['track']
		music_id_list.append(music_track['id'])
	return music_id_list

def get_track_data(track_id):
	meta = spotify.track(track_id)
	features = spotify.audio_features([track_id])
	#print(features)
	track_details = {
					 "acousticness": features[0]["acousticness"],
					 "album": meta['album']['name'],
					 "artist": meta['album']['artists'][0]['name'],
					 "durarion_in_minutes": round((meta['duration_ms'] * 0.001) / 60.0, 2),
					 "danceability": features[0]["danceability"],
					 "energy": features[0]["energy"],
					 "instrumentalness": features[0]["instrumentalness"],
					 "key": features[0]["key"],
					 "liveness": features[0]["liveness"],
					 "loudness": features[0]["loudness"],
					 "mode": features[0]["mode"],
					 "name": meta['name'],
					 "release_date": meta['album']['release_date'],
					 "speechiness": features[0]["speechiness"],
					 "tempo": features[0]["tempo"],
					 "valence": features[0]["valence"]
					}
	return track_details

playlist_id = input("Enter playlist id: ")
track_ids = get_track_ids(playlist_id)
print(len(track_ids))


tracks = []

acousticness = 0
danceability = 0
energy = 0
instrumentalness = 0
key = 0
loudness = 0
speechiness = 0
minors = 0
majors = 0

for i in range(len(track_ids)):
	time.sleep(.5)
	track = get_track_data(track_ids[i])
	tracks.append(track)

	acousticness += track["acousticness"]
	danceability += track["danceability"]
	energy += track["energy"]
	instrumentalness += track["instrumentalness"]
	key += track["key"]
	loudness += track["loudness"]
	speechiness += track["speechiness"]

	if track["mode"] == 0:
		minors += 1
	else:
		majors += 1

	print("Finished: " + str(i))

acousticness /= len(track_ids)
danceability /= len(track_ids)
energy /= len(track_ids)
instrumentalness /= len(track_ids)
key /= len(track_ids)
loudness /= len(track_ids)
speechiness /= len(track_ids)

with open('spotify_data.json', 'w') as outfile:
	json.dump(tracks, outfile, indent=4)

print("Average danceability (0.0 to 1.0):\t\t" + str(danceability))
print("Average energy (0.0 to 1.0):\t\t\t" + str(energy))
print("Average loudness (0 to -60): \t\t\t" + str(loudness))
print("Average speechiness (0.0 to -1.0): \t\t" + str(speechiness))
print("Average acousticness (0.0 to 1.0):\t\t" + str(acousticness))
print("Average instrumentalness (0.0 to 1.0):\t\t" + str(instrumentalness))
print("\n")
print("Average key is: \t\t\t\t" + str(key))
print("Number of songs in a major key: \t\t" + str(majors))
print("Number of songs in a minor key: \t\t" + str(minors))

