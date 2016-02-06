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
import scraper
import xml.etree.ElementTree as ET


BASE_URL = 'http://123movies.to'
PLAYLIST_URL1 = 'movie/loadEmbed/%s'
PLAYLIST_URL2 = 'movie/load_episode/%s'
SL_URL = '/movie/loadepisodes/%s'
Q_MAP = {'TS': QUALITIES.LOW, 'CAM': QUALITIES.LOW, 'HDTS': QUALITIES.LOW, 'HD-720P': QUALITIES.HD720}

class One23Movies_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return '123Movies'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            page_html = self._http_get(url, cache_limit=.5)
            movie_id = dom_parser.parse_dom(page_html, 'div', {'id': 'media-player'}, 'movie-id')
            if movie_id:
                server_url = SL_URL % (movie_id[0])
                url = urlparse.urljoin(self.base_url, server_url)
                html = self._http_get(url, cache_limit=.5)
                sources = {}
                for match in re.finditer('loadEpisode\(\s*(\d+)\s*,\s*(\d+)\s*\).*?class="btn-eps[^>]*>([^<]+)', html, re.DOTALL):
                    link_type, link_id, q_str = match.groups()
                    if link_type in ['12', '13', '14']:
                        url = urlparse.urljoin(self.base_url, PLAYLIST_URL1 % (link_id))
                        sources.update(self.__get_link_from_json(url, q_str))
                    else:
                        media_url = PLAYLIST_URL2 % (link_id)
                        headers = {'Referer': url}
                        url = urlparse.urljoin(self.base_url, media_url)
                        xml = self._http_get(url, headers=headers, cache_limit=.5)
                        sources.update(self.__get_links_from_xml(xml, video))
                
            for source in sources:
                if sources[source]['direct']:
                    host = self._get_direct_hostname(source)
                else:
                    host = urlparse.urlparse(source).hostname
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': sources[source]['quality'], 'views': None, 'rating': None, 'url': source, 'direct': sources[source]['direct']}
                hosters.append(hoster)
        return hosters

    def __get_link_from_json(self, url, q_str):
        sources = {}
        html = self._http_get(url, cache_limit=.5)
        js_result = scraper_utils.parse_json(html, url)
        if 'embed_url' in js_result:
            quality = Q_MAP.get(q_str.upper(), QUALITIES.HIGH)
            sources[js_result['embed_url']] = {'quality': quality, 'direct': False}
        return sources
    
    def __get_links_from_xml(self, xml, video):
        sources = {}
        try:
            root = ET.fromstring(xml)
            for item in root.findall('.//item'):
                title = item.find('title').text
                for source in item.findall('{http://rss.jwpcdn.com/}source'):
                    stream_url = source.get('file')
                    label = source.get('label')
                    if self._get_direct_hostname(stream_url) == 'gvideo':
                        quality = scraper_utils.gv_get_quality(stream_url)
                    elif label:
                        quality = scraper_utils.height_get_quality(label)
                    else:
                        quality = scraper_utils.blog_get_quality(video, title, '')
                    sources[stream_url] = {'quality': quality, 'direct': True}
                    log_utils.log('Adding stream: %s Quality: %s' % (stream_url, quality), log_utils.LOGDEBUG)
        except Exception as e:
            log_utils.log('Exception during 123Movies XML Parse: %s' % (e), log_utils.LOGWARNING)

        return sources
    
    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year):
        search_url = urlparse.urljoin(self.base_url, '/movie/search/')
        search_url += title
        html = self._http_get(search_url, cache_limit=1)
        results = []
        for item in dom_parser.parse_dom(html, 'div', {'class': 'ml-item'}):
            match_title = dom_parser.parse_dom(item, 'span', {'class': 'mli-info'})
            match_url = re.search('href="([^"]+)', item, re.DOTALL)
            match_year = re.search('class="jt-info">(\d{4})<', item)
            is_episodes = dom_parser.parse_dom(item, 'span', {'class': 'mli-eps'})
            
            if match_title and match_url and not is_episodes:
                match_title = match_title[0]
                match_title = re.sub('</?h2>', '', match_title)
                match_title = re.sub('\s+\d{4}$', '', match_title)
                url = urlparse.urljoin(match_url.group(1), 'watching.html')
                match_year = match_year.group(1) if match_year else ''

                if not year or not match_year or year == match_year:
                    result = {'title': match_title, 'year': match_year, 'url': scraper_utils.pathify_url(url)}
                    results.append(result)

        return results
