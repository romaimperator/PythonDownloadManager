# -*- Mode: Python; tab-width: 4 -*-
# ex: tabstop=4 expandtab

import os
import sys
import glib
from threading import Thread
from unwrapt.Download import download_url

class DownThread(Thread):
    """
        A thread implementation that will download the files from the url
        array.

        After the download is complete, the callback function will be called.
        Progress is displayed using the given gtk progress_bar object.
    """
    def __init__(self, url, progress_bar, callback):
        super(DownThread, self).__init__()
        self.pb = progress_bar
        self.url = url
        self.stop = False
        self.cb = callback


    def run(self):
        """
            Downloads all the files in the url array.
        """
        for (u in self.url):
            filename = u.rsplit("/", 1)[1]
            download_url(self.url, filename, progress=self.update_pb)
        self.cb(True)

    
    def update_pb(self, display, current, total):
        """
            Calls the idle_add method of the gtk library to update the
            progress bar. Also checks if the download should be stopped.
        """
        glib.idle_add(self.pb.set_fraction(current/float(total)))
        glib.idle_add(self.pb.set_text("%5sB / %5sB" % (format_number(current),
                                                        format_number(total))))
        if self.stop:
            sys.exit(0)


    def cancel(self):
        """
            When called sets the boolean to stop the thread.
        """
        self.stop = True
