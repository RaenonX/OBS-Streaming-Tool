import os

from config import get_config
from foobar2k import FB2KReader
from statictext import StaticTextReader
from ytdata import YoutubeDataAPIv3

__all__ = ["get_content"]


config = get_config()

# Initialize managers
fb2k = FB2KReader(config.get("Foobar2K", "Path"))
fb2k.start()
txt = StaticTextReader(config.get("StaticText", "Path"))
txt.start()
ytlive = YoutubeDataAPIv3(os.environ.get("YT_KEY"), os.environ.get("YT_VIDEO_ID"),
                          current_viewer_format="Youtube 現正觀看人數: {}")

input_idx = 0

# Functions to iterate to get inputs
input_fns = [
    fb2k.get_content,
    txt.get_content,
    ytlive.get_current_viewer
]


def get_content():
    global input_idx, input_fns

    while True:
        content = input_fns[input_idx]()

        if content:
            return content
        else:
            input_idx += 1
            if input_idx >= len(input_fns):
                input_idx = 0
            return ""
