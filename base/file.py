import abc
import time

from threading import Thread


class FileReader(abc.ABC):
    def __init__(self, path, end_none=True):
        self._file_path = path
        self._out_new = []
        self._out_stable = []
        self._out_idx = 0
        self._end_none = end_none
        self._reset_idx_()

    def _reset_idx_(self):
        if self._end_none:
            self._out_idx = -1
        else:
            self._out_idx = 0

    # noinspection PyMethodMayBeStatic
    def _get_status_(self, fs):
        return "1" in fs.readline()

    def _sanitize_new_(self):
        self._out_new = list(map(lambda x: x.replace("\n", ""), self._out_new))

    def _read_(self):
        while True:
            try:
                f = open(self._file_path, "rt", encoding="utf-8")
            except IOError:
                time.sleep(3)
            else:
                with f:
                    try:
                        # Check status
                        status = self._get_status_(f)
                        if not status:
                            self._read_flush_()
                            time.sleep(3)
                            continue

                        self._read_flush_(f.readlines())
                    except (UnicodeDecodeError, UnicodeEncodeError):
                        time.sleep(3)

    def _read_flush_(self, s=None):
        # Skip if the parameter passed in is None
        if s is None:
            self._out_stable = []
            self._reset_idx_()
            return

        # Set the new content
        self._out_new = s
        self._sanitize_new_()

        # If stable is empty, the newly passed in contents must be new
        if not self._out_stable:
            self._out_stable = self._out_new
            return

        if hash(tuple(self._out_new)) == hash(tuple(self._out_stable)):
            # Same content, wait for 3 secs to refresh
            time.sleep(3)
        else:
            # Different content, update the content and reset the status
            self._out_stable = self._out_new
            self._reset_idx_()

        # Reset the temp storage for new content
        self._out_new = []

    def get_content(self):
        if not self._out_stable:
            return None

        self._out_idx += 1
        if self._out_idx >= len(self._out_stable):
            self._reset_idx_()
            if self._end_none:
                return None

        return self._out_stable[self._out_idx]

    def start(self):
        Thread(target=self._read_).start()
