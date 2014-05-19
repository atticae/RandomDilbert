from datetime import date
import random
import urllib.request
import re
import threading
import collections

from gi.repository import Gtk, Gio, GObject

from gi.repository.GdkPixbuf import Pixbuf

image_result = collections.namedtuple('ImageResult', ['url', 'date', 'title'])


def get_random_dilbert_image():
    rand_date = random_date(date(year=1989,month=4,day=16),date.today())
    date_string = "%s-%s-%s" % (rand_date.year, rand_date.month, rand_date.day)
    url_to_dilbert_page = "http://www.dilbert.com/" + date_string
    page_contents = urllib.request.urlopen(url_to_dilbert_page).read().decode('utf-8')
    image_url = re.search('<a href="/strips/comic/.*?/"><img.*?src="(.*?)"[^<]*</a>', page_contents).group(1)
    image_url = "http://www.dilbert.com" + image_url

    return image_result(image_url, rand_date, date_string)


def pixbuf_from_url(url):
    image_data = urllib.request.urlopen(url)
    input_stream = Gio.MemoryInputStream.new_from_data(image_data.read(), None) 
    pixbuf = Pixbuf.new_from_stream(input_stream, None) 
    return pixbuf


def random_date(start,end):
    start_date = start.toordinal()
    end_date = end.toordinal()
    return date.fromordinal(random.randint(start_date, end_date))


class RandomDilbert:

    title = "RandomDilbert Client"

    def __init__(self):
        self.cached_image = None
        self.cached_title = None
        self.window = Gtk.Window()
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.set_default_size(670, 430)

        self.random_button = Gtk.Button("Random Image")
        self.random_button.connect("clicked", self.show_cached_image)

        self.image = Gtk.Image()
        self.start_cache_thread()
        self.show_cached_image()

        self.vbox = Gtk.VBox()
        self.vbox.pack_start(self.image, True, True, 0)
        self.vbox.pack_start(self.random_button, True, True, 0)
        
        self.window.add(self.vbox)
        
        self.window.connect("destroy", self.destroy_window)
    
    def show(self):
        self.window.show_all()
        Gtk.main()
    
    def destroy_window(self, widget=None, data=None):
        Gtk.main_quit()

    def activate_button(self):
        self.random_button.set_sensitive(True)

    def cache_image(self):
        res = get_random_dilbert_image()
        self.cached_image = pixbuf_from_url(res.url)
        self.cached_title = self.title + " " + res.title
        GObject.idle_add(self.activate_button)

    def start_cache_thread(self):
        self.thread = threading.Thread(target=self.cache_image,)
        self.thread.start()
        print("New Thread started")

    def show_cached_image(self, widget=None, data=None):
        self.random_button.set_sensitive(False)
        self.thread.join()
        print("joined")
        self.image.set_from_pixbuf(self.cached_image)
        self.window.set_title(self.cached_title)
        self.start_cache_thread()


if __name__ == "__main__":
    GObject.threads_init()
    RandomDilbert().show()