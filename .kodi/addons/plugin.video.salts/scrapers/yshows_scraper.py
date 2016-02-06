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
import urlparse

from salts_lib import dom_parser
from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import XHR
import scraper


BASE_URL = 'http://yshow.me'
LINK_URL = '/link/'

class YShows_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'yshows'

    def resolve_link(self, link):
        link_url = urlparse.urljoin(self.base_url, LINK_URL)
        data = {'id_link': link}
        html = self._http_get(link_url, data=data, headers=XHR, cache_limit=.25)
        match = re.search('<iframe[^>]+src="([^"]+)', html, re.I)
        if match:
            return match.group(1)

    def format_source_label(self, item):
        label = '[%s] %s ' % (item['quality'], item['host'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.25)
            data_ids = dom_parser.parse_dom(html, 'a', {'class': '[^"]*list-group-item[^"]*'}, 'data-id')
            hosts = dom_parser.parse_dom(html, 'a', {'class': '[^"]*list-group-item[^"]*'})
            for source in zip(data_ids, hosts):
                host = re.sub('<img[^>]+>\s*', '', source[1]).lower()
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': scraper_utils.get_quality(video, host, QUALITIES.HIGH), 'views': None, 'rating': None, 'url': source[0], 'direct': False}
                hosters.append(hoster)
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def _get_episode_url(self, show_url, video):
        show_url = urlparse.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, cache_limit=8)
        season_links = dom_parser.parse_dom(html, 'a', {'class': 'pull-right'}, 'href')
        for season_url in season_links:
            if '/season-%s/' % (video.season) in season_url:
                episode_pattern = 'href="([^"]+)(?:[^>]+>){3}\s*S%s\s*Epi\s*%s' % (video.season, video.episode)
                title_pattern = 'href="(?P<url>[^"]+)(?:[^>]+>){3}\s*S\d+\s*Epi\s*\d+\s*:\s*(?P<title>[^<]+)'
                return self._default_get_episode_url(season_url, video, episode_pattern, title_pattern)

    def search(self, video_type, title, year):
        search_url = urlparse.urljoin(self.base_url, '/search_ajax')
        data = {'query': title}
        html = self._http_get(search_url, data=data, headers=XHR, cache_limit=1)
        results = []
        for match in re.finditer('class="list-group-item"\s+href="([^"]+)">([^<]+)', html):
            url, match_title = match.groups()
            result = {'url': scraper_utils.pathify_url(url), 'title': match_title, 'year': ''}
            results.append(result)
        return results
