# -*- coding: utf-8 -*-
"""
Copyright (C) 2015

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>
"""

import urllib, urllib2, sys, re, os, unicodedata
import xbmc, xbmcgui, xbmcplugin, xbmcaddon

plugin_handle = int(sys.argv[1])
mysettings = xbmcaddon.Addon(id = 'plugin.video.anarchitv')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
getSetting = xbmcaddon.Addon().getSetting
enable_adult_section = mysettings.getSetting('enable_adult_section')

fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
iconpath = xbmc.translatePath(os.path.join(home, 'resources/icons/'))
icon = xbmc.translatePath(os.path.join(home, 'resources/icons/icon.png'))

xml_regex = '<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>'
m3u_thumb_regex = 'logo=[\'"](.*?)[\'"]'
group_title_regex = 'group-title=[\'"](.*?)[\'"]'
m3u_regex = '#(.+?),(.+)\s*(.+)\s*'
ondemand_regex = '[ON\'](.*?)[\'nd]'
yt = 'http://www.youtube.com'
m3u = 'http://anarchitv.gq/TV/IPTV'
text = 'http://pastebin.com/raw.php?i=DSzNKYuD'

					
def read_file(file):
    try:
        f = open(file, 'r')
        content = f.read()
        f.close()
        return content
    except:
        pass
		

def make_request(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
		response = urllib2.urlopen(req)	  
		link = response.read()
		response.close()  
		return link
	except urllib2.URLError, e:
		print 'We failed to open "%s".' % url
		if hasattr(e, 'code'):
			print 'We failed with error code - %s.' % e.code	
		if hasattr(e, 'reason'):
			print 'We failed to reach a server.'
			print 'Reason: ', e.reason

			
def main():
	addDir('[COLOR white][B]*עדכונים אחרונים*[/B][/COLOR]', yt, 3, '%s/announcements.png'% iconpath, fanart)
	addDir('[COLOR red][B]חיפוש ערוץ[/B][/COLOR]', 'searchlink', 99, '%s/search.png'% iconpath, fanart)
	if len(List) > 0:	
		addDir('[COLOR yellow][B]כל הערוצים[/B][/COLOR]', yt, 2, '%s/allchannels.png'% iconpath, fanart)
	if (len(List) < 1 ):		
		mysettings.openSettings()
		xbmc.executebuiltin("Container.Refresh")
	addDir('[COLOR green][B]ערוצי HD[/B][/COLOR]', 'ערוצי HD', 51, '%s/hd.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]ישראל[/B][/COLOR]', 'ישראל', 62, '%s/israel.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]ספורט[/B][/COLOR]', 'sport', 52, '%s/sports.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]חדשות[/B][/COLOR]', 'חדשות', 53, '%s/news.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]דוקומנטרי[/B][/COLOR]', 'documentary', 54, '%s/documentary.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]ילדים[/B][/COLOR]', 'ילדים', 56, '%s/family.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]סרטים[/B][/COLOR]', 'סרטים', 57, '%s/movies.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]מוזיקה[/B][/COLOR]', 'מוזיקה', 58, '%s/music.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]רדיו[/B][/COLOR]', 'רדיו', 61, '%s/radio.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]שפות זרות[/B][/COLOR]', 'שפות זרות', 64,'%s/international.png'% iconpath, fanart)
	
		
def removeAccents(s):
	return ''.join((c for c in unicodedata.normalize('NFD', s.decode('utf-8')) if unicodedata.category(c) != 'Mn'))
	
		
def search(): 	
	try:
		keyb = xbmc.Keyboard('', 'חיפוש') 
		keyb.doModal()
		if (keyb.isConfirmed()):
			searchText = urllib.quote_plus(keyb.getText()).replace('+', ' ')
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
	except:
		pass

def sport(): 	
	try:
		searchText = (u'ספורט')
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	

def HD(): 	
	try:
		searchText = '(HD)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	
def news(): 	
	try:
		searchText = (u'חדשות')
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	
	
def documentary(): 	
	try:
		searchText = (u'דוקומנטרי')
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	
	
def entertainment(): 	
	try:
		searchText = '(Entertainment)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	
	
def family(): 	
	try:
		searchText = (u'ילדים')
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass


		
def lifestyle(): 	
	try:
		searchText = '(Lifestyle)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass

		
	
def movie(): 	
	try:
		searchText = (u'סרטים')
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	


def music(): 	
	try:
		searchText = (u'מוזיקה')
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	

def ondemandmovies(): 	
	try:
		searchText = (u'סרטים')
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
	except:
		pass
	
def ondemandshows(): 	
	try:
		searchText = '(OnDemandShows)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
	except:
		pass
		

	
def twentyfour7(): 	
	try:
		searchText = '(RandomAirTime 24/7)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	

	
def radio(): 	
	try:
		searchText = (u'רדיו')
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	

	
def adult(): 	
	try:
		searchText = '(Adult)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	
	
	
def israel(): 	
	try:
		searchText = (u'ישראל')
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	

def international(): 	
	try:
		searchGerman = (u'גרמנית')
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchGerman, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchSpanish = (u'ספרדית')
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchSpanish, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchFrench = (u'צרפתית')
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchFrench, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchHindi = (u'הודית')
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchHindi, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchArabic = (u'ערבית')
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchArabic, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchUrdu = (u'גרוזינית')
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchUrdu, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchFarsi = (u'פרסית')
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchFarsi, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchPortuguese = (u'פורטוגזית')
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchPortuguese, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchKurdish = (u'כורדית')
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchKurdish, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchChinese = (u'סינית')
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchChinese, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchSomali = (u'סומלית')
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchSomali, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchRussian = (u'רוסית')
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchRussian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchAfrikaans = '(Afrikaans)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchAfrikaans, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchRomanian = '(Romanian)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchRomanian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchItalian = '(Italian)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchItalian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchIsraeli = '(Israeli)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchIsraeli, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchGreek = '(Greek)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchGreek, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchhungarian = '(Hungarian)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchHungarian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchTamil = '(Tamil)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchTamil, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchMacedonian = '(Macedonian)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchMacedonian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchIndian = '(Indian)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchIndian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchCatalan = '(Catalan)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchCatalan, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchJamaica = '(Jamaica)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchJamaica, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchUkrainian = '(Ukrainian)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchUkrainian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchVietamese = '(Vietamese)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchVietamese, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchMaltese = '(Maltese)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchMaltese, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchLithuanian = '(Lithuanian)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchLithuanian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchPolish = '(Polish)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchPolish, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchSlovenian = '(Slovenian)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchSlovenian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchDeutsch = '(Deutsch)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchDeutsch, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchDutch = '(Dutch)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchDutch, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchFilipino = '(Filipino)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchFilipino, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchMandarin = '(Mandarin)'
		if len(List) > 0:		
			content = make_request(List)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchFilipino, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	
		
def text_online():		
	content = make_request(text)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass

	
def m3u_online():		
	content = make_request(List)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
		
def m3u_playlist(name, url, thumb):	
	name = re.sub('\s+', ' ', name).strip()			
	url = url.replace('"', ' ').replace('&amp;', '&').strip()
	if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
		if 'logo' in thumb:
			thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')			
			addDir(name, url, '', thumb, thumb)			
		else:	
			addDir(name, url, '', icon, fanart)
	else:
		if 'youtube.com/watch?v=' in url:
			url = 'plugin://plugin.video.youtube/play/?video_id=%s' % (url.split('=')[-1])
		elif 'dailymotion.com/video/' in url:
			url = url.split('/')[-1].split('_')[0]
			url = 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=%s' % url	
		else:			
			url = url
		if 'logo' in thumb:				
			thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
			addLink(name, url, 1, thumb, thumb)			
		else:				
			addLink(name, url, 1, icon, fanart)	

def play_video(url):
	media_url = url
	item = xbmcgui.ListItem(name, path = media_url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	return

def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring)>= 2:
		params = sys.argv[2]
		cleanedparams = params.replace('?', '')
		if (params[len(params)-1] == '/'):
			params = params[0:len(params)-2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0]] = splitparams[1]
	return param

List = 'http://anarchitv.gq/TV/IPTV'
def addDir(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
		u = 'plugin://plugin.video.youtube/%s/%s/' % (url.split( '/' )[-2], url.split( '/' )[-1])
		ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
		return ok		
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
	return ok

def addLink(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	liz = xbmcgui.ListItem(name, iconImage = "DefaultVideo.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('', fanart)
	liz.setProperty('IsPlayable', 'true') 
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz)  
		
params = get_params()
url = None
name = None
mode = None
iconimage = None

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	name = urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode = int(params["mode"])
except:
	pass
try:
	iconimage = urllib.unquote_plus(params["iconimage"])
except:
	pass  

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)
print "iconimage: " + str(iconimage)		

if mode == None or url == None or len(url) < 1:
	main()

elif mode == 1:
	play_video(url)

elif mode == 2:
	m3u_online()
	
elif mode == 3:
	text_online()
	
	
elif mode == 51:
	HD()
		
elif mode == 52:
	sport()
	
elif mode == 53:
	news()
	
elif mode == 54:
	documentary()
	
elif mode == 55:
	entertainment()
	
elif mode == 56:
	family()
	
elif mode == 57:
	movie()
	
elif mode == 58:
	music()
	
elif mode == 59:
	ondemandmovies()
	
elif mode == 65:
	ondemandshows()
	
elif mode == 60:
	twentyfour7()
	
elif mode == 61:
	radio()
	
elif mode == 62:
	israel()

elif mode == 63:
	lifestyle()
	
elif mode == 64:
	international()
	
elif mode == 98:
	adult()
	
elif mode == 99:
	search()
	
xbmcplugin.endOfDirectory(plugin_handle)