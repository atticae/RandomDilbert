#!/usr/bin/env python
from gi.repository import Gtk, Gio
from gi.repository.GdkPixbuf import Pixbuf

import random
import urllib.request
import re

def pixbuf_from_url(url):
    image_data = urllib.request.urlopen(url)
    input_stream = Gio.MemoryInputStream.new_from_data(image_data.read(), None) 
    pixbuf = Pixbuf.new_from_stream(input_stream, None) 
    return pixbuf

class RandomDilbert:
    def __init__(self):
        self.window = Gtk.Window()
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.set_default_size(670, 430)
        self.window.set_title("RandomDilbert Client by GKBRK")
        
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
        year = random.choice(["2011", "2012", "2013"])
        month = random.choice(range(1, 13))
        day = random.choice(range(1, 29))
        url_to_dilbert_page = "http://www.dilbert.com/%s-%s-%s/" % (year, month, day)
        page_contents = urllib.request.urlopen(url_to_dilbert_page).read().decode('utf-8')
        image_url = re.search('<a href="/strips/comic/.*?/"><img onload=".*?" src="(.*?)" alt="The Official Dilbert Website featuring Scott Adams Dilbert strips, animations and more" border="0" /></a>', page_contents).group(1)
        image_url = "http://www.dilbert.com" + image_url
        #print image_url
        return image_url
    
    def show_random_image(self, widget=None, data=None):
        self.image.set_from_pixbuf(pixbuf_from_url(self.get_random_image()))

if __name__ == "__main__":
    RandomDilbert().show()
