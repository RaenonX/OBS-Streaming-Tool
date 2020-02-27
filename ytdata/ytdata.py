import sys

import requests

__all__ = ["YoutubeDataAPIv3"]


class YoutubeDataAPIv3:
    URL = "https://www.googleapis.com/youtube/v3/videos"

    def get_current_viewer_url(self):
        return f"{YoutubeDataAPIv3.URL}?part=liveStreamingDetails" \
               f"&id={self._api_key}&key={self._api_key}" \
               "&fields=items%2FliveStreamingDetails%2FconcurrentViewers"

    def __init__(self, api_key, video_id, *, current_viewer_format=None):
        if not api_key:
            print("Youtube Data API v3 - api_key cannot be empty.")
            sys.exit(1)
        if not video_id:
            print("Youtube Data API v3 - video_id cannot be empty.")
            sys.exit(1)

        self._api_key = api_key
        self._video_id = video_id
        self._current_viewer = 0
        self._current_viewer_acquired = False
        self._current_viewer_format = current_viewer_format or "{}"

    def _update_current_viewer_(self, d):
        data = d["items"]
        if not data:
            return

        data = data[0]
        data = data.get("liveStreamingDetails")
        if not data:
            return

        data = data.get("concurrentViewers")
        self._current_viewer = int(data)

    def get_current_viewer(self):
        """
        Return the current viewers with formatted string or `None`.

        After this was called once, the next return will be None.
        Then the call after that, the next return will become the formatted string again.
        """
        self._current_viewer_acquired = not self._current_viewer_acquired

        if not self._current_viewer_acquired:
            return None

        response = requests.get(self.get_current_viewer_url())
        if response.status_code == 200:
            self._update_current_viewer_(response.json())

        return self._current_viewer_format.format(self._current_viewer) if self._current_viewer > 0 else None
