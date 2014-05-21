import threading
import ComicUtils

from comicreader import DilbertReader, SMBCReader

from gi.repository import Gtk, Gio, GObject


class RandomDilbert:

    title = "RandomDilbert Client"
    dilbert = DilbertReader()
    smbc = SMBCReader()

    def __init__(self):
        self.cached_image = None
        self.cached_title = None
        self.window = Gtk.Window()
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.set_default_size(670, 430)

        scrolled_window = Gtk.ScrolledWindow()

        self.random_button = Gtk.Button("Random Image")
        self.random_button.connect("clicked", self.show_cached_image)

        self.image = Gtk.Image()
        self.start_cache_thread()
        self.show_cached_image()

        self.vbox = Gtk.VBox()
        self.vbox.pack_start(self.image, True, True, 0)
        self.vbox.pack_start(self.random_button, True, True, 0)
        
        scrolled_window.add_with_viewport(self.vbox)

        self.window.add(scrolled_window)
        
        self.window.connect("destroy", self.destroy_window)
    
    def show(self):
        self.window.show_all()
        Gtk.main()
    
    def destroy_window(self, widget=None, data=None):
        Gtk.main_quit()

    def activate_button(self):
        self.random_button.set_sensitive(True)

    def cache_image(self):
        res = self.smbc.get_random_image()
        self.cached_image = ComicUtils.pixbuf_from_url(res.url)
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