from gi.repository import Gtk, Gio
from gi.repository.GdkPixbuf import Pixbuf
from datetime import timedelta, date

import random
import urllib.request
import re


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
        self.window = Gtk.Window()
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.set_default_size(670, 430)
        
        self.image = Gtk.Image()
        self.show_random_image()
        
        self.random_button = Gtk.Button("Random Image")
        self.random_button.connect("clicked", self.show_random_image)
        
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
    
    def get_random_image(self):
        rand_date = random_date(date(year=1989,month=4,day=16),date.today())
        date_string = "%s-%s-%s" % (rand_date.year, rand_date.month, rand_date.day)
        url_to_dilbert_page = "http://www.dilbert.com/" + date_string
        page_contents = urllib.request.urlopen(url_to_dilbert_page).read().decode('utf-8')
        image_url = re.search('<a href="/strips/comic/.*?/"><img.*?src="(.*?)"[^<]*</a>', page_contents).group(1)
        image_url = "http://www.dilbert.com" + image_url

        self.window.set_title(self.title + " " + date_string)

        return image_url
    
    def show_random_image(self, widget=None, data=None):
        self.image.set_from_pixbuf(pixbuf_from_url(self.get_random_image()))

if __name__ == "__main__":
    RandomDilbert().show()
