"""
    SALTS XBMC Addon
    Copyright (C) 2014 tknorris

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import re
import urllib
import urlparse

from salts_lib import dom_parser
from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://film-streaming.in'

class FilmStreaming_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'FilmStreaming.in'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        return '[%s] %s' % (item['quality'], item['host'])

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            q_str = dom_parser.parse_dom(html, 'span', {'class': 'calidad\d*'})
            if q_str:
                if q_str[0].upper() == 'COMING SOON':
                    return hosters
                
                try:
                    quality = scraper_utils.height_get_quality(q_str[0])
                except:
                    quality = QUALITIES.HIGH
            else:
                quality = QUALITIES.HIGH
            fragment = dom_parser.parse_dom(html, 'div', {'id': 'player\d+'})
            if fragment:
                for match in re.finditer('<iframe[^>]+src="([^"]+)', fragment[0], re.I):
                    stream_url = match.group(1)
                    host = urlparse.urlparse(stream_url).hostname
                    hoster = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': False}
                    hosters.append(hoster)
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year):
        search_url = urlparse.urljoin(self.base_url, '/?s=')
        search_url += urllib.quote_plus('%s %s' % (title, year))
        html = self._http_get(search_url, cache_limit=.25)
        results = []
        for item in dom_parser.parse_dom(html, 'div', {'class': 'item'}):
            match = re.search('href="([^"]+).*?alt="([^"]+)', item, re.DOTALL)
            if match:
                url, match_title_year = match.groups()
                match = re.search('(.*?)(?:\s+\(?(\d{4})\)?)', match_title_year)
                if match:
                    match_title, match_year = match.groups()
                else:
                    match_title = match_title_year
                    year_fragment = dom_parser.parse_dom(item, 'span', {'class': 'year'})
                    if year_fragment:
                        match_year = year_fragment[0]
                    else:
                        match_year = ''
                
                if not year or not match_year or year == match_year:
                    result = {'url': scraper_utils.pathify_url(url), 'title': match_title, 'year': match_year}
                    results.append(result)
        return results
