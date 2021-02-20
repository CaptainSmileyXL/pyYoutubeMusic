# pyYoutubeMusic

Introduction:
-------------
This is a Python script that enables the download of music from YouTube videos
in mp3 format.  It then attempts to get the information about the metadata tags 
including the cover art.

It uses youtube-dl to get the music from the videos.  It then uses the ShazamAPI
to attempt to identify the song and gather the relivent tags and artwork.  We then
use eyed3 to modify the music tags.

The script can do individual songs or an entire playlist.


Supported Platforms
-------------------
```
Tested on python 3.9.1 on OS X but should work on any platform that supports
the requierments listed below.
```

Python Requirements:
--------------------
```
ShazamAPI (https://github.com/Numenorean/ShazamAPI)
eyed3 (https://github.com/nicfit/eyeD3)
```

Other Requirements:
-------------------
```
youtube-dl (https://youtube-dl.org)
ffmpeg (http://www.ffmpeg.org)
```

Usage:
------
```
python3 pyYoutubeMusic.py [options]
-p <is this a playlist 0 | 1>
-d <directory for music files>
-u <url for youtube video/playlist>
  
example:
python3 pyYoutubeMusic.py -p 0 -d "/Users/share/music" -u "https://www.youtube.com/watch?v=pEZIYGN5HIo"

***  The quotes are important  ***
```

Note:
-----
The ShazamAPI does its query in Russian.  To change the language you must
modify the api.py. The following is for US English:
```
File (on OSX): /Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/ShazamAPI/api.py
  LANG = 'en-US'
  TIME_ZONE = 'America/Chicago'
  API_URL = 'https://amp.shazam.com/discovery/v5/en-US/US/iphone/-/tag/%s/%s?sync=true&webv3=true&sampling=true&connected=&shazamapiversion=v3&sharehub=true&hubv5minorversion=v5.1&hidelb=true&video=v3'
```
To discover the proper format for your locale you can use the Web Developer->Network inspection
capability in Firefox (Safari has one too, not sure about other browsers) and watch the query
made on Shazam's website.

If the script fails to download the video's music, make sure you have updated to the latest version
of youtube-dl
