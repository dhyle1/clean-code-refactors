# Program is a class 'Playlist' with different attributes

from song import song # Importing the song class from a file called song.py

class Playlist:
    def __init__(self, list_name):
        # Constructor to create a playlist with a given name
        self._songs = []  # A list to store song objects
        self._name = list_name

    def _extract_title_artist(self, song):
        title, artist = song.string_to_file().strip().split(';', maxsplit=1)
        return title, artist

    def load_from_file(self):
        # Reads songs from a file and adds them to the playlist
        f = open(self._name + ".txt", "r")  # Opens the file for reading
        for line in f:
            all_data = line.strip().split(';')  # Split the line into title and artist
            title = all_data[0]
            artist = all_data[1]
            song = song(title, artist)  # Creates a song object
            self._songs.append(song)  # Adds the song object to the playlist
        f.close()  # Closes the file

    def add_song(self, new_song):
        # Adds a song to the playlist
        self._songs.append(new_song)

    def remove_song(self, song):
        # Removes a song from the playlist
        title, artist = self._extract_title_artist(song)

        for x in self._songs:
            title1, artist1 = self._extract_title_artist(x)
            if title == title1 and artist == artist1:
                self._songs.remove(x)  # Removes the song object from the playlist
                return

    def play_all(self):
        # Plays all songs in the playlist
        for x in self._songs:
            x.play()  # Plays each song in the playlist

    def find_song_by_title(self, title):
        # Finds a song in the playlist based on title
        for x in self._songs:
            if x.check_title(title):
                return x  # Returns the song object if the title matches
        return None  # Returns None if the song is not found

    def get_songs_by_artist(self, artist_name):
        # Gets all songs by a specific artist
        songs_by_artist = []

        for song in self._songs:
            if song.check_artist(artist_name):
                songs_by_artist.append(song)  # Adds the song object to the list

        return songs_by_artist  # Returns the list with songs by the specified artist

    def save_to_file(self):
        # Writes the playlist to a file and saves it to a file
        f = open(self._name + ".txt", "w")  # Opens the file for writing

        for song in self._songs:
            converted = song.string_to_file()
            split = converted.strip().split(';')
            title_of_song = split[0]
            artist_of_song = split[1]
            f.write(f'{title_of_song};{artist_of_song}\n')  # Writes the song to the file
        f.close()  # Closes the file







