from song import song

class Playlist:
    def __init__(self, list_name):
        self._songs = []
        self._name = list_name

    def _extract_title_artist(self, song_obj):
        title, artist = song_obj.string_to_file().strip().split(';', maxsplit=1)
        return title, artist

    def load_from_file(self):
        with open(self._name + '.txt', 'r') as f:
            for line in f:
                title, artist = line.strip().split(';', maxsplit=1)
                self._songs.append(song(title, artist))

    def add_song(self, new_song):
        self._songs.append(new_song)

    def remove_song(self, target_song):
        title, artist = self._extract_title_artist(target_song)

        for i, song_obj in enumerate(self._songs):
            candidate_title, candidate_artist = self._extract_title_artist(song_obj)
            if title == candidate_title and artist == candidate_artist:
                self._songs.pop(i)
                return

    def play_all(self):
        for song_obj in self._songs:
            song_obj.play()

    def find_song_by_title(self, title):
        for song_obj in self._songs:
            if song_obj.check_title(title):
                return song_obj
        return None

    def get_songs_by_artist(self, artist_name):
        return [
            song_obj
            for song_obj in self._songs
            if song_obj.check_artist(artist_name)
        ]

    def save_to_file(self):
        with open(self._name + '.txt', 'w') as f:
            for song_obj in self._songs:
                title, artist = self._extract_title_artist(song_obj)
                f.write(f'{title};{artist}\n')
        