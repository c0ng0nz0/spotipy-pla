import json
import time
import sys
from collections import defaultdict
from collections import OrderedDict

import json
import statistics
from collections import defaultdict

from openpyxl import Workbook
from openpyxl.chart import (
    LineChart,
    PieChart,
    Reference
)

from openpyxl.formatting.rule import ColorScaleRule

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())




# Method definitions
######################################################

def print_standard_row(sheet, row, title, value):
	sheet["B" + str(row)] = title
	sheet["C" + str(row)] = round(statistics.mean(value),3)
	sheet["D" + str(row)] = round(statistics.pstdev(value),3)
	return row + 1


def get_track_ids(playlist_id):
	music_id_list = []
	playlist = spotify.playlist(playlist_id)
	for item in playlist['tracks']['items']:
		music_track = item['track']
		music_id_list.append(music_track['id'])
	return music_id_list


def get_artist_genre(artist_id):
	artist = spotify.artist(artist_id)
	return artist["genres"]


def get_track_data(track_id):
	meta = spotify.track(track_id)
	features = spotify.audio_features([track_id])
	genres = get_artist_genre(meta["artists"][0]["id"])
	#print(features)
	track_details = [
					 ("name", meta['name']),
					 ("acousticness", features[0]["acousticness"]),
					 ("instrumentalness", features[0]["instrumentalness"]),
					 ("liveness", features[0]["liveness"]),
					 ("speechiness", features[0]["speechiness"]),
					 ("danceability", features[0]["danceability"]),
					 ("energy", features[0]["energy"]),
					 ("valence", features[0]["valence"]),
					 ("album", meta['album']['name']),
					 ("artist", meta['album']['artists'][0]['name']),
					 ("duration_in_minutes", round((meta['duration_ms'] * 0.001) / 60.0, 2)),
					 ("genres", genres),
					 ("key", features[0]["key"]),
					 ("mode", features[0]["mode"]),
					 ("popularity", meta["popularity"]),
					 ("release_date", meta['album']['release_date']),
					 ("tempo", features[0]["tempo"]),
					 ("loudness", features[0]["loudness"])
					]

	return OrderedDict(track_details)


def print_to_screen(tallied_lists, tallied_other):
	print("Average acousticness (0.0 to 1.0):\t\t" + str(round(statistics.mean(tallied_lists["acousticness"]),3)))
	print("Average danceability (0.0 to 1.0):\t\t" + str(round(statistics.mean(tallied_lists["danceability"]),3)))
	print("Average energy (0.0 to 1.0):\t\t\t" + str(round(statistics.mean(tallied_lists["energy"]),3)))
	print("Average instrumentalness (0.0 to 1.0):\t\t" + str(round(statistics.mean(tallied_lists["instrumentalness"]),3)))
	print("Average loudness (0 to -60): \t\t\t" + str(round(statistics.mean(tallied_lists["loudness"]),3)))
	print("Average popularity (0 to 100): \t\t\t" + str(round(statistics.mean(tallied_lists["popularity"]),3)))
	print("Average speechiness (0.0 to -1.0): \t\t" + str(round(statistics.mean(tallied_lists["speechiness"]),3)))
	print("\n")
	print("Average key is: \t\t\t\t" + str(tallied_lists["key"]))
	print("Number of songs in a major key: \t\t" + str(tallied_other["majors"]))
	print("Number of songs in a minor key: \t\t" + str(tallied_other["minors"]))
	print("\n")
	print("Genre Count")
	for k,v in tallied_other["genres"].items():
		print(k + ": " + str(v))


def save_to_JSON(tracks):
	with open('spotify_data.json', 'w') as outfile:
		json.dump(tracks, outfile, indent=4)


def save_to_excel(tracks,tallied_lists,tallied_other):

	# Workbook setup
	######################################################

	wb = Workbook()
	display_sheet = wb.active
	display_sheet.title = "Display"
	data_sheet = wb.create_sheet("Data")



	# Populate the Data sheet
	######################################################

	rows = []

	row_titles = []
	for title in tracks[0].keys():
		row_titles.append(title)
	rows.append(row_titles)

	row_values = []
	for track in tracks:
		for metric in track.values():
			if type(metric) == list:
				row_values.append(str(metric))
			else:
				row_values.append(metric)
		rows.append(row_values)
		row_values = []

	for row in rows:
	    data_sheet.append(row)



	######################################################

	display_sheet.column_dimensions['B'].width = 30
	display_sheet.column_dimensions['D'].width = 20

	display_sheet.conditional_formatting.add('C3:C11', ColorScaleRule(start_type='num', start_value=0, start_color='90D0FF',
																	 mid_type='num', mid_value=.5, mid_color='FFFFFF', 
																	 end_type='num', end_value=1, end_color='FF9090'))

	display_sheet.conditional_formatting.add('D3:D11', ColorScaleRule(start_type='num', start_value=0, start_color='90D0FF',
																	 mid_type='num', mid_value=.25, mid_color='FFFFFF', 
																	 end_type='num', end_value=.5, end_color='FF9090'))



	# Populate the Display sheet
	# Left Side
	######################################################

	current_row = 2

	display_sheet["B" + str(current_row)] = "Metric"
	display_sheet["C" + str(current_row)] = "Mean"
	display_sheet["D" + str(current_row)] = "Standard Diviation"

	current_row += 1

	current_row = print_standard_row(display_sheet, current_row, "Danceability (0.0 to 1.0):", tallied_lists["danceability"])
	current_row = print_standard_row(display_sheet, current_row, "Energy (0.0 to 1.0):", tallied_lists["energy"])
	current_row = print_standard_row(display_sheet, current_row, "Valence (0.0 to 1.0):", tallied_lists["valence"])

	current_row += 2

	current_row = print_standard_row(display_sheet, current_row, "Acousticness (0.0 to 1.0):", tallied_lists["acousticness"])
	current_row = print_standard_row(display_sheet, current_row, "Instrumentalness (0.0 to 1.0):", tallied_lists["instrumentalness"])
	current_row = print_standard_row(display_sheet, current_row, "Liveness (0.0 to 1.0):", tallied_lists["liveness"])
	current_row = print_standard_row(display_sheet, current_row, "Speechiness (0.0 to 1.0):", tallied_lists["speechiness"])

	current_row += 2

	current_row = print_standard_row(display_sheet, current_row, "Duration (in minutes):", tallied_lists["duration"])
	current_row = print_standard_row(display_sheet, current_row, "Popularity (0 to 100):", tallied_lists["popularity"])
	current_row = print_standard_row(display_sheet, current_row, "*Loudness (0 to -60):", tallied_lists["loudness"])

	current_row += 2

	key_chart = LineChart()
	key_chart.title = "Key Chart"
	key_chart.style = 13
	key_chart.width = 12
	key_chart.y_axis.title = 'Key (Pitch Class Notation)'
	key_chart.x_axis.title = 'Track Number'
	data = Reference(data_sheet, min_col=13, min_row=2, max_row=len(rows))
	key_chart.add_data(data, titles_from_data=False)
	display_sheet.add_chart(key_chart, "B" + str(current_row))

	current_row += 18

	display_sheet["B" + str(current_row)] = "Number of songs in a major key:"
	display_sheet["C" + str(current_row)] = tallied_other["majors"]

	current_row += 1

	display_sheet["B" + str(current_row)] = "Number of songs in a minor key:"
	display_sheet["C" + str(current_row)] = tallied_other["minors"]

	current_row += 3

	display_sheet["B" + str(current_row)] = "Genre"
	display_sheet["C" + str(current_row)] = "Count"

	current_row += 1

	sorted_genres = {k: v for k, v in sorted(tallied_other["genres"].items(), key=lambda item: item[1], reverse=True)}

	for k,v in sorted_genres.items():
		display_sheet["B" + str(current_row)] = k
		display_sheet["C" + str(current_row)] = v
		current_row += 1

	pie_max_row = 0
	if (len(sorted_genres)) > 15:
		pie_max_row = current_row + (15 - len(sorted_genres))
	else:
		pie_max_row = current_row



	# Populate the Display sheet
	# Right Side
	######################################################

	pie = PieChart()
	labels = Reference(display_sheet, min_col=2, min_row=current_row-len(sorted_genres), max_row=pie_max_row)
	data = Reference(display_sheet, min_col=3, min_row=current_row-len(sorted_genres), max_row=pie_max_row)
	pie.add_data(data, titles_from_data=True)
	pie.set_categories(labels)
	pie.title = "Top Artist Genres (Up to 15)"

	display_sheet.add_chart(pie, "G45")


	emo_chart = LineChart()
	emo_chart.height = 10
	emo_chart.width = 20
	emo_chart.title = "Emotional Qualities"
	emo_chart.style = 13
	emo_chart.y_axis.title = 'Value: 0 - 1'
	emo_chart.x_axis.title = 'Track Number'
	data = Reference(data_sheet, min_col=6, min_row=1, max_col=8, max_row=len(rows))
	emo_chart.add_data(data, titles_from_data=True)

	# Style the lines
	emo_chart.series[0].graphicalProperties.line.solidFill = "00CC00"
	emo_chart.series[1].graphicalProperties.line.solidFill = "FF0000"
	emo_chart.series[2].graphicalProperties.line.solidFill = "0000FF"

	display_sheet.add_chart(emo_chart, "G2")


	perf_chart = LineChart()
	perf_chart.height = 10
	perf_chart.width = 20
	perf_chart.title = "Performative Qualities"
	perf_chart.style = 13
	perf_chart.y_axis.title = 'Value: 0 - 1'
	perf_chart.x_axis.title = 'Track Number'
	data = Reference(data_sheet, min_col=2, min_row=1, max_col=5, max_row=len(rows))
	perf_chart.add_data(data, titles_from_data=True)

	# Style the lines
	perf_chart.series[0].graphicalProperties.line.solidFill = "0033FF"
	perf_chart.series[1].graphicalProperties.line.solidFill = "993300"
	perf_chart.series[2].graphicalProperties.line.solidFill = "009900"
	perf_chart.series[3].graphicalProperties.line.solidFill = "FFCC00"

	display_sheet.add_chart(perf_chart, "G24")



	# Save workbook
	######################################################

	wb.save("output.xlsx")




def main():

	# Get the data
	######################################################

	playlist_id = input("Enter playlist id: ")
	track_ids = get_track_ids(playlist_id)
	print(len(track_ids))

	tracks = []

	for i in range(len(track_ids)):
		time.sleep(.25)
		track = get_track_data(track_ids[i])
		tracks.append(track)
		print("Grabbed song #" + str(i))

	# Tally the numbers
	######################################################

	tallied_lists = {
		
		"acousticness": [],
		"danceability": [],
		"duration": [],
		"energy": [],
		"instrumentalness": [],
		"key": [],
		"liveness": [],
		"loudness": [],
		"popularity": [],
		"speechiness": [],
		"valence": []
	}

	tallied_other = {

		"genres": defaultdict(lambda:0),
		"minors": 0,
		"majors": 0

	}


	for i in range(len(tracks)):
		track = tracks[i]

		tallied_lists["acousticness"].append(track["acousticness"])
		tallied_lists["danceability"].append(track["danceability"])
		tallied_lists["duration"].append(track["duration_in_minutes"])
		tallied_lists["energy"].append(track["energy"])
		tallied_lists["instrumentalness"].append(track["instrumentalness"])
		tallied_lists["key"].append(track["key"])
		tallied_lists["liveness"].append(track["liveness"])
		tallied_lists["loudness"].append(track["loudness"])
		tallied_lists["popularity"].append(track["popularity"])
		tallied_lists["speechiness"].append(track["speechiness"])
		tallied_lists["valence"].append(track["valence"])

		if track["mode"] == 0:
			tallied_other["minors"] += 1
		else:
			tallied_other["majors"] += 1

		for genre in track["genres"]:
			tallied_other["genres"][genre] += 1

	if len(sys.argv) == 1:
		print_to_screen(tallied_lists,tallied_other)

	elif sys.argv[1] == "text":
		print_to_screen(tallied_lists,tallied_other)

	elif sys.argv[1] == "json":
		save_to_JSON(tracks)

	elif sys.argv[1] == "excel":
		save_to_excel(tracks,tallied_lists,tallied_other)

	elif sys.argv[1] == "all":
		print_to_screen(tallied_lists,tallied_other)
		save_to_JSON(tracks)
		save_to_excel(tracks,tallied_lists,tallied_other)

	else:
		print("Yo - the possible arguments are \"text\", \"json\", \"excel\", or \"all\".")


if __name__ == "__main__":
    main()






