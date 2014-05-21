import re

from ComicUtils import *


class DilbertReader:

    def get_random_image(self):
        rand_date = random_date(date(year=1989,month=4,day=16),date.today())
        date_string = "%s-%s-%s" % (rand_date.year, rand_date.month, rand_date.day)
        url_to_dilbert_page = "http://www.dilbert.com/" + date_string
        page_contents = urllib.request.urlopen(url_to_dilbert_page).read().decode('utf-8')
        image_url = re.search('<a href="/strips/comic/.*?/"><img.*?src="(.*?)"[^<]*</a>', page_contents).group(1)
        image_url = "http://www.dilbert.com" + image_url

        return image_result(image_url, rand_date, date_string)


class SMBCReader:

    host = "http://www.smbc-comics.com/"

    def __init__(self):
        page_contents = urllib.request.urlopen(self.host).read().decode('utf-8')
        result = re.search("Math.random\(\)\*([0-9]+)", page_contents).group(1)
        self.maxid = int(result)

    def get_random_image(self):
        random_id = random.randint(1,self.maxid)
        url_to_dilbert_page = self.host + "?id=" + str(random_id) + "#comic"
        page_contents = urllib.request.urlopen(url_to_dilbert_page).read().decode('utf-8')
        image_url = re.search('<div id="comicimage">[^<]*<img src=\'([^\']+)\'>', page_contents).group(1)

        return image_result(image_url, date=None, title=str(random_id))
