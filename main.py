from pytube import YouTube

url = 'https://www.youtube.com/watch?v=U0kCRbSyjmo'


def on_download_progress(stream, chunk, bytes_remaining):
    bytes_downloaded = stream.filesize - bytes_remaining
    percentage = bytes_downloaded * 100 / stream.filesize

    print(f'Downloading... {int(percentage)}%')


yt = YouTube(url)
yt.register_on_progress_callback(on_download_progress)
video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

print("Loading...")

video.download()
