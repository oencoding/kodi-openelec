import re

domain="http://mangafox.me"
encoding="utf-8"

def run(hash,ump,referer=None):
	pg=ump.get_page(domain+hash,encoding)
	img=re.findall('img src="(.*?)"',pg)
	return {"img":img[0]}
	