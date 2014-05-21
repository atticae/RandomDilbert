from datetime import date
import random
import urllib.request
import collections

from gi.repository.GdkPixbuf import Pixbuf

from gi.repository import Gio



image_result = collections.namedtuple('ImageResult', ['url', 'date', 'title'])

def pixbuf_from_url(url):
    image_data = urllib.request.urlopen(url)
    input_stream = Gio.MemoryInputStream.new_from_data(image_data.read(), None)
    pixbuf = Pixbuf.new_from_stream(input_stream, None)
    return pixbuf


def random_date(start,end):
    start_date = start.toordinal()
    end_date = end.toordinal()
    return date.fromordinal(random.randint(start_date, end_date))
