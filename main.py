from spotify_playlist import SpotifyPlaylist
from yt_downloader import YoutubeDownloader
from youtube_search import YoutubeSearch

from os import listdir, getcwd, remove
from tkinter import Tk, Entry, Label, Button, filedialog, Text, END
from threading import Thread
from pickle import load
from setton.utils import decodifica


class App:
    """
    O App permite que você escolha uma playlist do Spotify e baixa os videos/audios do Youtube.
    """
    def __init__(self):
        self.janela = Tk(screenName="Spotify Playlist Downloader")
        self.janela.title("Spotify Downloader")
        self.janela['bg'] = '#dca'
        self.janela.geometry("350x400+100+100")

        # Id Group
        Label(self.janela, text='ID da playlist', background=self.janela['bg']).place(x=120, y=10)
        self.id_input = Entry(self.janela, text='', font="Calibri 12", highlightbackground='#777777',
                              background='#e0e0ff', width=27)
        self.id_input.place(x=50, y=30)

        # Directory Group
        self.output_folder = getcwd()
        self.output_chooser = Button(self.janela, text="Selecionar pasta", command=self.choose)
        self.output_chooser.place(x=180, y=100)
        self.output_chooser = Label(self.janela, text='...' + self.output_folder[-38:])
        self.output_chooser.place(x=50, y=70)

        # Download Button
        Button(self.janela, background="#0d0", text="Download", command=lambda: Thread(target=self.download).start())\
            .place(x=120, y=140)

        # Log Report
        self.logs = Text(self.janela, background="#fff", width=40, height=10)
        self.logs.place(x=15, y=180)

        self.logs.tag_configure("red", foreground="#f00")
        self.logs.tag_configure("green", foreground="#0f0")
        self.logs.tag_configure("blue", foreground="#00f")

        self.janela.mainloop()

    def log(self, *texts):
        self.logs.insert(END, ' '.join(texts) + '\n\n')

    def choose(self):
        self.output_folder = filedialog.askdirectory()
        if len(self.output_folder) > 20:
            self.output_chooser['text'] = '...' + self.output_folder[-38:]
        else:
            self.output_chooser['text'] = self.output_folder

    def download(self):
        self.logs.delete('1.0', END)
        self.log("Starting downloads...")
        try:
            musicas = SpotifyPlaylist(self.id_input.get())
        except RuntimeError as msg:
            self.logs.tag_add("red", "1.0", END)
            self.log(str(msg))
            return
        done = 0

        # Progress
        Label(self.janela, width=40, background='#fff').place(x=20, y=350)
        progress_bar = Label(self.janela, width=0, background='#8fa')
        progress_bar.place(x=20, y=350)
        percent = Label(self.janela, text="0%")
        percent.place(x=140, y=350)

        for name, artist in musicas:
            # Update Counters
            done += 1
            tag_indexes = (f"{done * 2 + 1}.0", f"{done * 2 + 1}.100")

            # Update Progress
            progress_bar['width'] = int(40 * done / len(musicas))
            percent['text'] = f"{(done / len(musicas) * 100):.1f}%"

            # Download
            if f"{name.replace(':', '').replace('/', '').replace(',', '').replace('?', '').replace('.', '')}.mp4" \
                    in listdir(self.output_folder):
                self.log(name, 'já existe')
                self.logs.tag_add("blue", *tag_indexes)
                continue
            try:
                video = YoutubeSearch(name + artist, max_results=5).videos[0]
            except KeyError:
                self.log(f"Erro ao baixar {name}")
                self.logs.tag_add("red", *tag_indexes)
                continue
            url = "https://www.youtube.com" + video['url_suffix']
            YoutubeDownloader(url, name, self.output_folder)
            self.log("Baixado:", name)
            self.logs.tag_add("green", *tag_indexes)


if __name__ == '__main__':
    # 'cache.pickle' contains the encrypted CLIENT information and cache data
    with open("cache.pickle", 'rb') as file:
        env, cache = load(file).values()
        with open(".env", 'w') as env_file:
            env_file.write(decodifica(env, 1, 1))
        with open(".cache", 'w') as cache_file:
            cache_file.write(decodifica(cache, 1, 1))
    App()
    remove(".env")
    remove(".cache")
