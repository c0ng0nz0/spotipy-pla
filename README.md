# spotipy-pla
A Spotify playlist analyzer that I'm whipping up for fun, primarily using Spotipy.

I'll just say right now that currently this is incredibly beta, and I guarantee that if you try to run this, it probably won't work like you're expecting.

## Installation

You'll need to run this in a python environment that has the "spotipy" package installed. I like creating virtual environments for this sort of thing.

```
python3 -m venv ve
source ve/bin/activate
pip install spotipy
```

Once that's set up, clone the repo / copy the file / retype it by hand in vi / whatever so that you have a local copy.

```
git clone https://github.com/c0ng0nz0/spotipy-pla.git
```

In order to run this script, you'll need Spotify Developer API app credentials. Those aren't super hard to get, just log into 
https://developer.spotify.com/dashboard/ and create a new app. What I've decided to to is create a single app for all my Spotipy developement. You'll 
need a client ID and client secret. They are each 32 hex character strings.

Now, I've decided to not hardcode those into my scripts. What I think is a cool idea is the store them as environment variables. If you created a
virtual environment using the above commands, you can actually go the the bottom of the `ve/bin/activate` file and add whatever commands to create
those environment variables. I use a Mac, so that means using `export`.

```
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

Once those are in place, you can leave (if needed) and re-enter your virtual envrionment, and everything is good to go.

```
deactivate
source ve/bin/activate
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
python splaz.py
Enter playlist id: 5d3LhoHMBPuQ2tSbvjfn2j
17
Finished: 0
Finished: 1
Finished: 2
Finished: 3
Finished: 4
Finished: 5
Finished: 6
Finished: 7
Finished: 8
Finished: 9
Finished: 10
Finished: 11
Finished: 12
Finished: 13
Finished: 14
Finished: 15
Finished: 16
Average danceability (0.0 to 1.0):		0.439
Average energy (0.0 to 1.0):			0.770764705882353
Average loudness (0 to -60): 			-7.115235294117647
Average speechiness (0.0 to -1.0): 		0.06366470588235294
Average acousticness (0.0 to 1.0):		0.05561476470588236
Average instrumentalness (0.0 to 1.0):		0.2049450429411765


Average key is: 				5.705882352941177
Number of songs in a major key: 		12
Number of songs in a minor key: 		5
```

You'll also get a json file that contains each of the attributes listed for each song.

