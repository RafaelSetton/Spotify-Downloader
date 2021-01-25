from pytube import YouTube, StreamQuery, Stream
from os.path import dirname


class YoutubeDownloader:
    def __init__(self, video_link, output_name=None, output_path=dirname(__file__)):
        video = YouTube(video_link)
        best_stream = self.get_best(video.streams)

        if not output_name:
            output_name = best_stream.title

        best_stream.download(output_path=output_path, filename=output_name)

    @staticmethod
    def get_best(streams: StreamQuery) -> Stream:
        return streams.filter(subtype='mp4').get_highest_resolution()

