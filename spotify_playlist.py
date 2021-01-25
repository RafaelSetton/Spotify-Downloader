import spotipy
from dotenv import load_dotenv
from os import getenv


class SpotifyPlaylist:
    def __new__(cls, playlist_id: str, *args, **kwargs) -> list[tuple[str, str]]:
        load_dotenv()
        client_id = getenv("CLIENT_ID")
        client_secret = getenv("CLIENT_SECRET")

        redirect_uri = 'http://somandosaber.com.br/'
        scope = 'user-library-read playlist-read-private'

        auth_manager = spotipy.SpotifyOAuth(scope=scope, client_id=client_id,
                                            client_secret=client_secret, redirect_uri=redirect_uri)
        sp = spotipy.Spotify(auth_manager=auth_manager)

        try:
            pl = sp.playlist(playlist_id)['tracks']['items']
        except spotipy.SpotifyException:
            raise RuntimeError("ID da playlist inválido!")

        nome_artista = map(lambda musica: (musica['track']['name'], musica['track']['artists'][0]['name']), pl)

        return list(nome_artista)
