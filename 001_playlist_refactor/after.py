# Program is a class 'Playlist' with different attributes

from song import song # Importing the song class from a file called song.py

class Playlist:
    def __init__(self, list_name):
        # Constructor to create a playlist with a given name
        self._songs = []  # A list to store song objects
        self._name = list_name

    def _extract_title_artist(self, song_obj):
        title, artist = song_obj.string_to_file().strip().split(';', maxsplit=1)
        return title, artist

    def load_from_file(self):
        # Reads songs from a file and adds them to the playlist
        with open(self._name + ".txt", "r") as f:
            for line in f:
                title, artist = line.strip().split(';', maxsplit=1)
                self._songs.append(song(title, artist))

    def add_song(self, new_song):
        # Adds a song to the playlist
        self._songs.append(new_song)

    def remove_song(self, target_song):
        # Removes a song from the playlist
        title, artist = self._extract_title_artist(target_song)

        for song_obj in self._songs:
            candidate_title, candidate_artist = self._extract_title_artist(song_obj)
            if title == candidate_title and artist == candidate_artist:
                self._songs.remove(song_obj)  # Removes the song object from the playlist
                return

    def play_all(self):
        # Plays all songs in the playlist
        for song_obj in self._songs:
            song_obj.play()  # Plays each song in the playlist

    def find_song_by_title(self, title):
        # Finds a song in the playlist based on title
        for song_obj in self._songs:
            if song_obj.check_title(title):
                return song_obj  # Returns the song object if the title matches
        return None  # Returns None if the song is not found

    def get_songs_by_artist(self, artist_name):
        # Gets all songs by a specific artist
        songs_by_artist = []

        for song_obj in self._songs:
            if song_obj.check_artist(artist_name):
                songs_by_artist.append(song_obj)  # Adds the song object to the list

        return songs_by_artist  # Returns the list with songs by the specified artist

    def save_to_file(self):
        # Writes the playlist to a file and saves it to a file
        with open(self._name + ".txt", "w") as f:
            for song_obj in self._songs:
                title, artist = self._extract_title_artist(song_obj)
                f.write(f'{title};{artist}\n')
        







