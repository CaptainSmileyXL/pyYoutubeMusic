#!/usr/local/bin/python3

##  Author: CaptainSmiley
##  Date:   2/18/2021
##  License:    Creative Commons Zero v1.0 Universal


from ShazamAPI import Shazam
import eyed3
import urllib.request
import subprocess
import sys
import ssl
import os
from os import walk
import getopt


issues = ""


def get_album_image(imageurl):
    if imageurl is None:
        print("problem with image URL!")
    else:
        print('Getting album cover: ', imageurl)
        ssl._create_default_https_context = ssl._create_unverified_context
        urllib.request.urlretrieve(imageurl, './album.jpg')


def write_tags(song, title, song_artist, album, song_genre, album_artist):
    global issues

    print("Writing song file tags")

    audiofile = eyed3.load(song)
    audiofile.tag.artist = song_artist
    audiofile.tag.album = album
    audiofile.tag.album_artist = album_artist
    audiofile.tag.title = title
    audiofile.tag.genre = song_genre

    if os.path.exists("album.jpg"):
        audiofile.tag.images.set(3, open('album.jpg', 'rb').read(), 'image/jpeg')
    else:
        issues += " No album cover"

    audiofile.tag.save()

    if os.path.exists("album.jpg"):
        os.remove('album.jpg')


def get_song_info(song):
    global issues

    title = None
    song_artist = None
    album = None
    song_genre = None
    album_artist = None
    image_url = None

    print("Getting song info")

    mp3_file_content_to_recognize = open(song, 'rb').read()
    shazam = Shazam(mp3_file_content_to_recognize)
    recognize_generator = shazam.recognizeSong()

    d = next(recognize_generator)
    for var in range(len(d)):
        if isinstance(d[var], dict):
            matches = d[var].get('matches')
            if not matches:
                break

            tdict = d[var].get('track')
            title = tdict.get("title")
            if title is None:
                issues += "No title, "

            song_artist = tdict.get("subtitle")
            if song_artist is None:
                issues += "No song artist, "

            for item in tdict.get("sections"):
                if isinstance(item, dict):
                    metadata = item.get("metadata")
                    if metadata is not None:
                        for a in metadata:
                            album = a.get("text")
                            break

#           print('Sections: ', tdict.get("sections"))
            genres = tdict.get("genres")
            if genres is None:
                song_genre = ""
                issues += "No genres, "
            else:
                song_genre = genres.get("primary")

            urlparams = tdict.get("urlparams")
            if isinstance(urlparams, dict):
                album_artist = list(urlparams.values())[-1]
                album_artist = album_artist.replace("+", " ")

            idict = tdict.get("images")
            if isinstance(idict, dict):
                image_url = idict.get("coverart")

    return title, song_artist, album, song_genre, album_artist, image_url


def analyze_songs(directory):
    global issues
    problems = []

    print("analyzing songs")

    _, _, filenames = next(walk(directory))

    for song in filenames:
        issues = ""

        if song.startswith('.'):
            continue

        if song == 'album.jpg':
            continue

        if song in sys.argv[0]:
            continue

        print(song)

        s = directory+'/'+song
        title, song_artist, album, song_genre, album_artist, image_url = get_song_info(s)

        #  song isnt found
        if not title:
            e = song + '****: song not found!'
            problems.append(e)
            continue

        #  other things not found
        if not album:
            issues += " No album"

        if image_url:
            get_album_image(image_url)

        print('Title: ', title)
        print('Subtitle: ', song_artist)
        print('Album: ', album)
        print('Genres: ', song_genre)
        print('Artist: ', album_artist)

        write_tags(s, title, song_artist, album, song_genre, album_artist)

        if issues:
            e = song + '****: ' + issues
            problems.append(e)

    print("\n\nFile analysis and updating complete.")

    if problems:
        print("Problems found:")
        for i in problems:
            print('\t', i)
    else:
        print("\tNo problems found!")



def get_music(url, directory, isPlaylist):
    print("Getting music...")

    if not isPlaylist:
        ret = subprocess.run(["/usr/local/bin/youtube-dl", "--no-check-certificate", "--ignore-errors", "--format", "bestaudio", "--extract-audio", "--audio-format", "mp3", "--audio-quality", "192K", "--output", directory+"/'%(title)s.%(ext)s'", url], capture_output=True, text=True) 
        print("stdout: ", ret.stdout)
        print("stderr: ", ret.stderr)
    elif isPlaylist:
        ret = subprocess.run(["/usr/local/bin/youtube-dl", "--no-check-certificate", "--ignore-errors", "--format", "bestaudio", "--extract-audio", "--audio-format", "mp3", "--audio-quality", "192K", "--output", directory+"/'%(title)s.%(ext)s'", "--yes-playlist", url], capture_output=True, text=True) 
        print("stdout: ", ret.stdout)
        print("stderr: ", ret.stderr)


def main(argv):
    isPlaylist = 0
    directory = ""
    music_url = ""

    try:
        opts, args = getopt.getopt(argv, "hp:d:u:")
    except getopt.GetoptError:
        print(sys.argv[0], ' [-p <is url a playlist 0|1>] -d <direcotry for music files> [-u <youtube url>]')
        print("*** make sure you have quotes around the directory and URL")
        print("*** make sure you have the latest version of youtube-dl")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(sys.argv[0], ' [-p <is url a playlist 0|1>] -d <direcotry for music files> [-u <youtube url>]')
            sys.exit()
        elif opt == '-p':
            isPlaylist = arg
        elif opt == '-d':
            directory = arg
        elif opt == '-u':
            music_url = arg

    if music_url:
        if not directory:
            print("REQUIRED:  no directory specified")
            sys.exit(-1)
        else:
            get_music(music_url, directory, isPlaylist)
    else:
        print("no url specified")

    if directory:
        analyze_songs(directory)
    else:
        print("REQUIRED:  no directory specified")
        sys.exit(-1)


if __name__ == '__main__':
    main(sys.argv[1:])
