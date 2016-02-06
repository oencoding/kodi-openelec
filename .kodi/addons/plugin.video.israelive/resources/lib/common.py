# -*- coding: utf-8 -*-
import sys, os, io, re, time, base64, random, hashlib, zipfile
import urllib, urllib2, json
import xbmc, xbmcgui, xbmcaddon
import multiChoiceDialog
import itertools, operator

AddonID = "plugin.video.israelive"
Addon = xbmcaddon.Addon(AddonID)
AddonName = "IsraeLIVE"
localizedString = Addon.getLocalizedString
user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
favoritesFile = os.path.join(user_dataDir, 'favorites.txt')
remoteSettingsFile = os.path.join(user_dataDir, "remoteSettings.txt")
listsDir = os.path.join(user_dataDir, 'lists')
if not os.path.exists(listsDir):
	os.makedirs(listsDir)

def isFileOld(file, deltaInSec):
	lastUpdate = 0 if not os.path.isfile(file) else int(os.path.getmtime(file))
	now = int(time.time())
	isFileNotUpdate = True if (now - lastUpdate) > deltaInSec else False 
	return isFileNotUpdate
	
def GetSubKeyValue(remoteSettings, key, subKey):
	return remoteSettings[key][subKey] if (remoteSettings.has_key(key) and remoteSettings[key].has_key(subKey)) else None
	
def UpdateFile(file, key, remoteSettings=None, zip=False, forceUpdate=False):
	if remoteSettings is None:
		remoteSettings = ReadList(os.path.join(user_dataDir, "remoteSettings.txt"))
	
	if remoteSettings == []:
		return False
			
	lastModifiedFile = "{0}LastModified.txt".format(file[:file.rfind('.')])
	if (zip == False and not os.path.isfile(file)) or not os.path.isfile(lastModifiedFile):
		fileContent = "0"
	else:
		f = open(lastModifiedFile,'r')
		fileContent = f.read()
		f.close()
	last_modified = GetSubKeyValue(remoteSettings, key, "lastModified")
	
	isNew = forceUpdate or last_modified is None or (fileContent < last_modified)
	if not isNew:
		return False
	
	urls = GetSubKeyValue(remoteSettings, key, "urls")
	if urls is None or len(urls) == 0:
		return False
		
	random.seed()
	random.shuffle(urls)
	url = Decode(urls[0])
	
	response = None
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0')
		req.add_header('Referer', 'http://www.IsraeLIVE.org/')
		response = urllib2.urlopen(req)
	
		if zip:
			urllib.urlretrieve(url, file)
		else:
			data = response.read().replace('\r','')
			f = open(file, 'w')
			f.write(data)
			f.close()
		
		response.close()

	except Exception as ex:
		print ex
		if not response is None:
			response.close()
		return False

	if key == "remoteSettings":
		remoteSettings = json.loads(data)
		last_modified = GetSubKeyValue(remoteSettings, key, "lastModified")
		
	f = open(lastModifiedFile, 'w')
	f.write(last_modified)
	f.close()
	
	return True
	
def ReadList(fileName):
	try:
		with open(fileName, 'r') as handle:
			content = json.load(handle)
	except Exception as ex:
		print ex
		content=[]

	return content

def WriteList(filename, list, indent=True):
	try:
		with io.open(filename, 'w', encoding='utf-8') as handle:
			if indent:
				handle.write(unicode(json.dumps(list, indent=2, ensure_ascii=False)))
			else:
				handle.write(unicode(json.dumps(list, ensure_ascii=False)))
		success = True
	except Exception as ex:
		print ex
		success = False
		
	return success
	
def GetUnSelectedList(fullList, selectedList):
	unSelectedList = []
	for index, item in enumerate(fullList):
		if not any(selectedItem["id"] == item.get("id", "") for selectedItem in selectedList):
			unSelectedList.append(item)
	return unSelectedList
	
def GetUpdatedList(file, key, remoteSettings=None, forceUpdate=False):
	UpdateFile(file, key, remoteSettings=remoteSettings, forceUpdate=forceUpdate)
	return ReadList(file)
	
def UpdateZipedFile(file, key, remoteSettings=None, forceUpdate=False):
	zipFile = "{0}.zip".format(file[:file.rfind('.')])
	if UpdateFile(zipFile, key, remoteSettings=remoteSettings, zip=True, forceUpdate=forceUpdate):
		xbmc.executebuiltin("XBMC.Extract({0}, {1})".format(zipFile, user_dataDir), True)
		try:
			os.remove(zipFile)
		except:
			pass
		return True
	return False
	
def GetEncodeString(str):
	try:
		import chardet
		str = str.decode(chardet.detect(str)["encoding"]).encode("utf-8")
	except:
		try:
			str = str.encode("utf-8")
		except:
			pass
	return str

def UpdateFavouritesFromRemote():
	remoteFavouritesType = Addon.getSetting("remoteFavouritesType")
	if remoteFavouritesType == "1" or remoteFavouritesType == "2":
		if remoteFavouritesType == "1":
			try:
				req = urllib2.Request(Addon.getSetting("remoteFavouritesUrl"))
				req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0')
				responseData = urllib2.urlopen(req).read().replace('\r','')
				remoteFavouritesList = json.loads(responseData)
			except Exception as ex:
				print ex
				remoteFavouritesList = []
		elif remoteFavouritesType == "2":
			remoteFavouritesList = ReadList(Addon.getSetting("remoteFavouritesFile"))
			
		favoritesList = ReadList(favoritesFile)
		if remoteFavouritesList != [] and cmp(favoritesList, remoteFavouritesList) != 0:
			WriteList(favoritesFile, remoteFavouritesList)
			return True
	return False
		
def UpdatePlx(file, key, remoteSettings=None, refreshInterval=0, forceUpdate=False):
	if remoteSettings is None:
		remoteSettings = ReadList(os.path.join(user_dataDir, "remoteSettings.txt"))
	if remoteSettings == []:
		return False
	isListUpdated = False
	if UpdateFavouritesFromRemote():
		isListUpdated = True
	if isFileOld(file, refreshInterval):
		isListUpdated = True
	lastModifiedFile = os.path.join(user_dataDir, "chLastModified.txt")
	if not os.path.isfile(lastModifiedFile):
		old_modified = "0"
	else:
		f = open(lastModifiedFile,'r')
		old_modified = f.read()
		f.close()
	new_modified = GetSubKeyValue(remoteSettings, "ch", "lastModified")
	isNew = forceUpdate or new_modified is None or (old_modified < new_modified)
	if not isNew:
		return False
	if not new_modified is None:
		data = GetSubKeyValue(remoteSettings, "ch", "content")
		f = open(file, 'w')
		f.write(base64.b64decode(data))
		f.close()
		f = open(lastModifiedFile, 'w')
		f.write(new_modified)
		f.close()

	if isListUpdated:
		fullList = GetListFromPlx(fullScan=True)
		fullList.sort(key=operator.itemgetter('group'))
		categories_list = []
		for key, group in itertools.groupby(fullList, lambda item: item["group"]):
			list1 = [{"url": item["url"], "image": item["image"], "name": item["name"].decode("utf-8"), "type": item["type"], "group": item["group"].decode("utf-8"), "id": item["id"]} for item in group]
			filename = os.path.join(listsDir, "{0}.list".format(key.strip()))
			WriteList(filename, list1)
			categories = [{"name": item["name"], "image": item["image"], "group": item["group"], "id": item["id"]} for item in list1 if item['type'] == "playlist"]
			if len(categories) > 0:
				for category in categories:
					categories_list.append(category)

		categories_list.sort(key=operator.itemgetter('id'))
		WriteList(os.path.join(listsDir, "categories.list"), categories_list)
		
		selectedCatList = ReadList(os.path.join(listsDir, "selectedCategories.list"))
		for index, cat in enumerate(selectedCatList):
			if any(f["id"] == cat.get("id", "") for f in categories_list):
				categoty = [f for f in categories_list if f["id"] == cat.get("id", "")]
				selectedCatList[index] = categoty[0]
			else:
				selectedCatList[index]["type"] = "ignore"
		WriteList(os.path.join(listsDir, "selectedCategories.list"), selectedCatList)
		
		favsList = ReadList(favoritesFile)
		for index, favourite in enumerate(favsList):
			if any(f["id"] == favourite.get("id", "") for f in fullList):
				channel = [f for f in fullList if f["id"] == favourite.get("id", "")]
				favsList[index] = {"url": channel[0]["url"], "image": channel[0]["image"], "name": channel[0]["name"].decode("utf-8"), "type": channel[0]["type"], "group": channel[0]["group"].decode("utf-8"), "id": channel[0]["id"]}
			else:
				if favsList[index].has_key("id"):
					favsList[index]["type"] = "ignore"
		WriteList(favoritesFile, favsList)
	return isListUpdated
		
def OKmsg(title, line1, line2="", line3=""):
	dlg = xbmcgui.Dialog()
	dlg.ok(title, line1, line2, line3)
	
def GetKeyboardText(title = "", defaultText = ""):
	keyboard = xbmc.Keyboard(defaultText, title)
	keyboard.doModal()
	text = "" if not keyboard.isConfirmed() else keyboard.getText()
	return text
	
def YesNoDialog(title, line1, line2="", line3="", nolabel="No", yeslabel="Yes"):
	dialog = xbmcgui.Dialog()
	ok = dialog.yesno(title, line1=line1, line2=line2, line3=line3, nolabel=nolabel, yeslabel=yeslabel)
	return ok
	
def GetMenuSelected(title, list, autoclose=0):
	dialog = xbmcgui.Dialog()
	answer = dialog.select(title, list, autoclose=autoclose)
	return answer

def GetMultiChoiceSelected(title, list):
	dialog = multiChoiceDialog.MultiChoiceDialog(title, list)
	dialog.doModal()
	selected = dialog.selected[:]
	del dialog #You need to delete your instance when it is no longer needed because underlying xbmcgui classes are not grabage-collected. 
	return selected
	
def GetLogoFileName(item):
	if item.has_key('image') and item['image'] is not None and item['image'] != "":
		ext = item['image'][item['image'].rfind('.')+1:]
		i = ext.rfind('?')
		if i > 0: 
			ext = ext[:ext.rfind('?')]
		if len(ext) > 4:
			ext = "png"
		tvg_logo = hashlib.md5(item['image'].strip()).hexdigest()
		logoFile = "{0}.{1}".format(tvg_logo, ext)
	else:
		logoFile = ""
		
	return logoFile

def Decode(string, key=None):
	if key is None:
		key = GetKey()
	decoded_chars = []
	string = base64.urlsafe_b64decode(string.encode("utf-8"))
	for i in xrange(len(string)):
		key_c = key[i % len(key)]
		decoded_c = chr(abs(ord(string[i]) - ord(key_c) % 256))
		decoded_chars.append(decoded_c)
	decoded_string = "".join(decoded_chars)
	return decoded_string
	
def GetKey():
	return AddonName
	
def GetAddonDefaultRemoteSettingsUrl():
	remoteSettingsUrl = ""
	try:
		f = open(os.path.join(Addon.getAddonInfo("path").decode("utf-8"), 'resources', 'settings.xml') ,'r')
		data = f.read()
		f.close()
		matches = re.compile('setting id="remoteSettingsUrl".+?default="(.+?)"',re.I+re.M+re.U+re.S).findall(data)
		remoteSettingsUrl = matches[0]
	except Exception as ex:
		print ex
	return remoteSettingsUrl
	
def GetRemoteSettings():
	remoteSettingsUrl = Addon.getSetting("remoteSettingsUrl")
	if Addon.getSetting("forceRemoteDefaults") == "true":
		defaultRemoteSettingsUrl = GetAddonDefaultRemoteSettingsUrl()
		if (defaultRemoteSettingsUrl != "") and (defaultRemoteSettingsUrl != remoteSettingsUrl):
			remoteSettingsUrl = defaultRemoteSettingsUrl
			Addon.setSetting("remoteSettingsUrl", remoteSettingsUrl)
			
	remoteSettings = ReadList(remoteSettingsFile)
	if remoteSettings == []:
		remoteSettings = {}

	urls = GetSubKeyValue(remoteSettings, "remoteSettings", "urls")
	if urls is None or len(urls) == 0:
		remoteSettings = {"remoteSettings": {"urls": remoteSettingsUrl.split(","), "lastModified": "0", "refresh": 12}}
	
	return remoteSettings

def GetListFromPlx(filterCat="9999", includeChannels=True, includeCatNames=True, fullScan=False):
	plxFile = os.path.join(user_dataDir, "israelive.plx")
	f = open(plxFile,'r')
	data = f.read()
	f.close()
	
	matches = re.compile('^type(.+?)#$',re.I+re.M+re.U+re.S).findall(data)
	categories = ["9999"]
	list = []
	for match in matches:
		item=re.compile('^(.*?)=(.*?)$',re.I+re.M+re.U+re.S).findall("type{0}".format(match))
		item_data = {}
		for field, value in item:
			item_data[field.strip().lower()] = value.strip()
		if not item_data.has_key("type"):
			continue
		
		url = item_data['url']
		thumb = "" if not item_data.has_key("thumb") else item_data['thumb']
		channelName = GetEncodeString(item_data['name'])
		
		if item_data["type"] == 'audio' and item_data["url"] == '':
			if channelName.find("-") != 0:
				categories.append(item_data["id"])
				item_data["type"] = "playlist"
				if not includeCatNames:
					continue
			else:
				del categories[-1]
				continue
		elif not includeChannels:
			continue
		
		lenCat = len(categories)
		subCat = categories[lenCat-1] if item_data["type"] != "playlist" else categories[lenCat-2]

		if subCat == filterCat or fullScan:
			list.append({"url": url, "image": thumb, "name": channelName, "type": item_data["type"], "group": subCat, "id": item_data["id"]})
		
	return list
	
def GetChannels(categoryID):
	fileName = os.path.join(listsDir, "{0}.list".format(categoryID))if categoryID != "Favourites" else favoritesFile
	return ReadList(fileName)

def MakeCatGuides(categories, epg):
	for category in categories:
		MakeCatGuide(category["id"], epg)
	
def MakeCatGuide(categoryID, epg):
	filename = os.path.join(listsDir, "{0}.guide".format(categoryID))
	channels = GetChannels(categoryID)
	categoryEpg = []
	for channel in channels:
		if channel["type"] == 'video' or channel["type"] == 'audio':
			channelName = channel['name'].encode("utf-8").replace("[COLOR yellow][B]", "").replace("[/B][/COLOR]", "")
			try:
				ch = [x for x in epg if x["channel"].encode('utf-8') == channelName]
				if not any(d.get('channel', '').encode('utf-8') == channelName for d in categoryEpg):
					categoryEpg.append(ch[0])
			except Exception, e:
				pass
	WriteList(filename, categoryEpg, indent=False)
	
def MakeFavouritesGuide(fullGuideFile, epg=None):
	if epg is None:
		epg = ReadList(fullGuideFile)
	MakeCatGuide("Favourites", epg)
			
def GetGuide(categoryID):
	fileName = os.path.join(listsDir, "{0}.guide".format(categoryID))
	return ReadList(fileName)
	
def ExtractAll(_in, _out):
	try:
		zin = zipfile.ZipFile(_in, 'r')
		zin.extractall(_out)
		zin.close()
	except Exception, e:
		print str(e)
		return False
	return True
	
def InstallAddon(addonID):
	try:
		req = urllib2.Request('https://github.com/cubicle-vdo/xbmc-israel/raw/master/addons.xml')
		response = urllib2.urlopen(req)
		data = response.read()
		response.close()
		data = re.compile('<addon id="(.+?)".+?version="(.+?)"', re.I+re.M+re.U+re.S).findall(data)
		for i in range(len(data)):
			if data[i][0] == addonID:
				addonVer = data[i][1]
				break
		addonsDir = xbmc.translatePath(os.path.join('special://home', 'addons')).decode("utf-8")
		url = 'https://github.com/cubicle-vdo/xbmc-israel/raw/master/repo/{0}/{0}-{1}.zip'.format(addonID, addonVer)
		packageFile = os.path.join(addonsDir, 'packages', 'isr.zip')
		urllib.urlretrieve(url, packageFile)
		if ExtractAll(packageFile, addonsDir):
			try:
				os.remove(packageFile)
			except:
				pass
		else:
			raise Exception("--- Can't extract package. ")
				
		xbmc.executebuiltin("UpdateLocalAddons")
		xbmc.executebuiltin("UpdateAddonRepos")
	except Exception as ex:
		print ex
		return False

	return True
	
def CheckNewVersion(remoteSettings):
	versionFile = os.path.join(user_dataDir, "addonVersion.txt")
	if not os.path.isfile(versionFile):
		version = ""
	else:
		f = open(versionFile,'r')
		version = f.read()
		f.close()
	newVersion = Addon.getAddonInfo("version")
	
	resolverVerFile = os.path.join(user_dataDir, "resolverVersion.txt")
	if not os.path.isfile(resolverVerFile):
		resolverVersion = ""
	else:
		f = open(resolverVerFile,'r')
		resolverVersion = f.read()
		f.close()
		
	resolverNewVersion = ""
	try:
		resolverNewVersion = xbmcaddon.Addon("script.module.israeliveresolver").getAddonInfo("version")	
	except:
		if InstallAddon('script.module.israeliveresolver'):
			try:
				resolverNewVersion = xbmcaddon.Addon("script.module.israeliveresolver").getAddonInfo("version")	
			except:
				pass
			#OKmsg(localizedString(30236).encode('utf-8'), localizedString(30201).encode('utf-8'))
		else:
			OKmsg(localizedString(30237).encode('utf-8'), localizedString(30238).encode('utf-8'))
			return
	
	isUpdated = False
	if resolverNewVersion > resolverVersion:
		isUpdated = True
		title = "{0}{1}".format(localizedString(30235).encode('utf-8'), resolverNewVersion)
		f = open(resolverVerFile, 'w')
		f.write(resolverNewVersion)
		f.close()
	
	if newVersion > version:
		isUpdated = True
		title = "{0}{1}".format(localizedString(30200).encode('utf-8'), newVersion)
		f = open(versionFile, 'w')
		f.write(newVersion)
		f.close()
	
	CheckNewResolver(remoteSettings)
	
	if isUpdated and Addon.getSetting("useIPTV") == "true":
		OKmsg(title, localizedString(30201).encode('utf-8'))

def CheckNewResolver(remoteSettings):
	try:
		newModified = GetSubKeyValue(remoteSettings, "resolver", "lastModified")
		resolverContent = Decode(GetSubKeyValue(remoteSettings, "resolver", "content"))
		resolverDir = xbmc.translatePath(xbmcaddon.Addon("script.module.israeliveresolver").getAddonInfo('path')).decode("utf-8")
		resolverFile = os.path.join(resolverDir, 'lib', 'myResolver.py')
		lastModifiedFile = os.path.join(user_dataDir, 'resolverLastModified.txt')
		if not os.path.isfile(lastModifiedFile):
			lastModified = "0"
		else:
			f = open(lastModifiedFile, 'r')
			lastModified = f.read()
			f.close()
		if newModified is not None and resolverContent is not None and lastModified < newModified:
			f = open(resolverFile, 'w')
			f.write(resolverContent)
			f.close()
			f = open(lastModifiedFile, 'w')
			f.write(newModified)
			f.close()
	except Exception as ex:
		print ex

def GetLivestreamerPort():
	portNum = 65007
	try:
		portNum = int(Addon.getSetting("LiveStreamerPort"))
	except:
		pass
	return portNum