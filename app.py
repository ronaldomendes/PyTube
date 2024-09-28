import os
import sys
import time

import streamlit as st
import streamlit.components.v1 as com
from pytube import YouTube
from streamlit import runtime
from streamlit.web import cli


def main():
    st.set_page_config(page_title='PyTube Video Downloader')
    html_code = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        h1 {text-align: center;}
        h5 {color: #F4A875;}
        div.block-container{padding: 2rem;}
    </style>
    <h1>PyTube Video Downloader</h1>
    """
    st.markdown(html_code, unsafe_allow_html=True)
    st.markdown('---')

    def clear_text():
        st.session_state["url"] = ""

    def on_download_progress(stream, chunk, bytes_remaining):
        video_size = stream.filesize
        bytes_downloaded = video_size - bytes_remaining
        percentage = bytes_downloaded * 100 / video_size
        result = int(percentage)
        progress_bar.progress(result, text=str(f'{result} %'))

    url = st.text_input(label='Paste your YouTube video URL:', key='url')

    col1, col2 = st.columns(2)
    with col1:
        clear = st.button(label='Clear', use_container_width=True, on_click=clear_text)
    with col2:
        download = st.button(label='Download', use_container_width=True)

    if len(url) > 0:
        link = url.split('=')[1].split('&')[0]
        com.iframe(src=f"https://www.youtube.com/embed/{link}", width=670, height=390)

    if download:
        yt = YouTube(url, on_progress_callback=on_download_progress)
        progress_text = "Download in progress. Please wait."
        progress_bar = st.progress(0, text=progress_text)

        path_container = st.empty()

        try:
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            main_path = os.path.expanduser(os.getenv('USERPROFILE')).replace('\\', '/')
            user_path = f"{main_path}/Downloads/{yt.author}"

            with path_container.container():
                st.success(f"Saving your video in: {user_path}")

            video.download(output_path=user_path)
        except Exception as e:
            st.error(f'Error: {e}')
        time.sleep(2)
        progress_bar.empty()
        path_container.empty()


if __name__ == '__main__':
    if runtime.exists():
        main()
    else:
        sys.argv = ['streamlit', 'run', sys.argv[0]]
        sys.exit(cli.main())
