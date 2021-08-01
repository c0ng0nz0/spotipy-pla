# spotipy-pla
A Spotify playlist analyzer that I'm whipping up for fun, primarily using Spotipy.


## Update

OK I HAVE MODERATE CONFIDENCE that if you run this script it will do something in the realm of your expectations.

Won't go into many details, but this is a python script to take a look at some of the data that Spotify maintains on *most every song in their library*. It grabs analytical measurements such as the "enegry", "valence", or "speechiness" of a song. There's also other cool stuff to pull like duration, popularity, artist genres (they also have album genres as a separate field but it doen't look super populated), etc. 

Here's more info:
https://developer.spotify.com/discover/

This script pulls that data for every song on a playlist, makes it available to people, and does some ... "light analytics". I'm not a statistician yo - I just push buttons.

## Installation

If you know the word Python is more than just a type of boop noodle, but haven't actually "used" the Python programming langauge to do stuff, here's a short crash course.

https://c0ng0nz0.github.io/2021/07/30/Installing-Python.html

You'll need to have python3 installed, and run it from an environment that has the "spotipy" and "openpyxl" packages. 

```
pip install spotipy
pip install openpyxl
```

Use a virtual environment or don't, I'm not your mother.

## Authentication

In order to run this script, you'll need Spotify Developer API app credentials. Those aren't super hard to get, just log into 
https://developer.spotify.com/dashboard/ and create a new app. What I've decided to do is create a single app for all my Spotipy developement. You'll 
need a client ID and client secret. They are each 32 hex character strings.

The script will prompt you for that information if you don't want to mess with environment variables. 

But if you do, and have a virtual environment set up ....

You can actually go the the bottom of the `bin/activate` file and add whatever commands to create those environment variables. Here's an example I use on my Mac.

```
vim ve/bin/active
...
# This should detect bash and zsh, which have a hash command that must
# be called to get it to forget past commands.  Without forgetting
# past commands the $PATH changes we made may not be respected
if [ -n "${BASH:-}" -o -n "${ZSH_VERSION:-}" ] ; then
    hash -r
fi

# Spotipy Creds

SPOTIPY_CLIENT_ID='1234567890abcdef1234567890abcdef' # Example data used, put replace it with your own client ID
export SPOTIPY_CLIENT_ID
SPOTIPY_CLIENT_SECRET='1234567890abcdef1234567890abcdef' # Example data used, put replace it with your own client secret
export SPOTIPY_CLIENT_SECRET
```

## Running

Running the script will prompt you for a playlist ID. This can be found in the URL for the playlist, here's an example:
```
https://open.spotify.com/playlist/5d3LhoHMBPuQ2tSbvjfn2j?si=dbbda1946a794628
```

The playlist ID is the portion after "playlist/" and before the URL parameters (the question mark). In the above example the ID is:
`5d3LhoHMBPuQ2tSbvjfn2j`

Here is an example of it running:

```
python whatever.py
# You may also get prompted for the Spotify API credentials here
Enter playlist id: 2fgBaTw3YbvsVymdXHpf1M
16
Finished: 0
Finished: 1
--skip--
Finished: 15
Average acousticness (0.0 to 1.0):		0.12609762500000002
Average danceability (0.0 to 1.0):		0.5351874999999999
Average energy (0.0 to 1.0):			0.6963125000000001
Average instrumentalness (0.0 to 1.0):	0.47476000000000007
Average loudness (0 to -60): 			-7.7108125
Average popularity (0 to 100): 			31.25
Average speechiness (0.0 to -1.0): 		0.07400625


Average key is: 				6.5625
Number of songs in a major key: 		4
Number of songs in a minor key: 		12


Genre Count
edm: 7
pop dance: 6
progressive house: 5
progressive trance: 5
trance: 6
uplifting trance: 4
big beat: 1
```
You can also create a JSON file, an Excel workbook, or all of the above:
```
python splaz.py json
python splaz.py excel
python splaz.py all
```

The Excel document has a few tables and charts taht might or might not be useful, and all the data in another sheet.

![table](https://user-images.githubusercontent.com/3879630/127781323-ee110f46-09fd-449b-b32f-fbc2f9d8bb6b.png)
![chart](https://user-images.githubusercontent.com/3879630/127781324-a1bf8519-9353-4f92-afe2-dccc8935b86a.png)
