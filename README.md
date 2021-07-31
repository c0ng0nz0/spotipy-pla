# spotipy-pla
A Spotify playlist analyzer that I'm whipping up for fun, primarily using Spotipy.


## Update

OK I HAVE MODERATE CONFIDENCE that if you run this script it will do something in the realm of your expectations.

Won't go into many details, but this is a python script to take a look at some of the data that Spotify maintains on *most every song in their library*. It grabs analytical measurements such as the "enegry", "valence", or "speechiness" of a song. There's also other cool stuff to pull like duration, popularity, artist genres (they also have album genres as a separate field but it doen't look super populated), etc. This script pulls that data for every song on a playlist, makes it available to people, and does some ... "light analytics".

I'm not a statistician yo - I just push buttons, and just barely do that. This is not a perfect project by far, but it will get the job done.

I've also taken a shot at making this more available to people who have never used Python before, and might be using Windows. It's not *super informative* and may require some Googling. I actually haven't used Python on Windows in years, but I think the instructions below work.

## Installation

You'll need to have python3 installed, and run it from an environment that has the "spotipy" and "openpyxl" packages. I like creating virtual environments for this sort of thing. It let's me keep my Python environments a little cleaner - but is totally optional.

``` 
# From a bash shell: You may need to grab python3 yourself somehow
# For Windows: Install from the website, and ... just skip the first two commands, it'll be fine
python3 -m venv ve
source ve/bin/activate
pip install spotipy
pip install openpyxl
pip install maybe-there's-another-one.not-a-100%here
```
If you understand Git ... you don't need my advice.

If you're like "I'd rather not", cheers. Copy and paste "splaz.py" into "whatever.py", which is in a directory you can run the "python" command from. You can use NotePad if you want .... buuuuuut ...... if you ever do this with any frequency I'd recommend installing NotePad++.

In order to run this script, you'll need Spotify Developer API app credentials. Those aren't super hard to get, just log into 
https://developer.spotify.com/dashboard/ and create a new app. What I've decided to to is create a single app for all my Spotipy developement. You'll 
need a client ID and client secret. They are each 32 hex character strings.

Now, I've decided to not hardcode those into my scripts because I'm pretty sure that's 30 lashes. What I think is a cool idea is the store them as environment variables. 

### If you created a virtual environment using the above commands...
You can actually go the the bottom of the `ve/bin/activate` file and add whatever commands to create those environment variables. I use a Mac, so that means using `export`.

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
Once those are in place, you can leave (if needed) and re-enter your virtual envrionment, and everything is good to go.
```
deactivate
source ve/bin/activate
```
### If you did not, and are probably using Windows
Ok - you've got two options here. You can either place the credentials you have into variables in the script and change it use that inforamtion. And despite what everyone in the security community might say (that it's a bad practice - which it is), the chances of it becoming an issue are slim at best. The .. "adjective" way to do it would be to set those values as environment variables. And creating windows environment variables called SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET isn't super hard.


## Running

Running the script will prompt you for a playlist ID. This can be found in the URL for the playlist, here's an example:
```
https://open.spotify.com/playlist/5d3LhoHMBPuQ2tSbvjfn2j?si=dbbda1946a794628
```

The playlist ID is the portion after "playlist/" and before the URL parameters (the question mark). In the above example the ID is:
`5d3LhoHMBPuQ2tSbvjfn2j`

Here is an example of it running:

```
python test.py
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





