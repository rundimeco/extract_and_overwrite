#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import urllib2
import zipfile
import ConfigParser

def extract(path,url):
        success = False
        config_proxy = "proxy"
        if os.path.exists(config_proxy):
            f = open(config_proxy,'r')
            proxies = eval(f.read())
            f.close()
        else:
            proxies = {}
	if proxies:
            proxy = urllib2.ProxyHandler(proxies)
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)
            with open(path,'wb') as f:
                f.write(urllib2.urlopen(url).read())
                f.close()
                success = True
	return success

def unzip(path,dest):
  try:
    Z = zipfile.ZipFile(path, "r")
    Z.extractall(dest)
    zipOK = True
  except:
		zipOK = False
  return zipOK

def get_options(couples):
	liste_zips = ["Base_blitz","FFE_70"]
	liste_config = {"path":["cheminZIP"],"dest":["cheminFILES"],"url":["url"]}

	has_config = False

	for z in liste_zips:
		for nom ,infos in liste_config.iteritems():
			try:
				option = config.get(z,infos[0])
				couples[z][nom] = option
				has_config = True
			except:
				pass
	return couples,has_config

couples = {"Base_blitz":{"url":"http://www.echecs.asso.fr/Papi/Blitz.zip",
            "path":"./",
            "dest":"./outputs/",
            "filename":"base_blitz.zip"},
	"FFE_70":{
            "url":"http://www.echecs.asso.fr/papi/ffe70.zip",
            "path":"./",
	    "dest":"./outputs/",
	    "filename":"FFE_70.zip"}}
try:
  config = ConfigParser.RawConfigParser()
  c= config.read('config.txt')
  print "\nOptions configurées dans le fichier:\t%s\n"%c[0]
  couples,has_config = get_options(couples)
except:
	print "\nErreur dans la lecture du fichier de configuration, options par défaut utilisées\n"
	
for nom,infos in couples.iteritems():
	url = infos['url']
	filename=infos['filename']
	dest = infos['dest']
	path = infos['path']+filename
        print "\nDémarrage du téléchargement de %s"%url
	success = extract(path,url)
	if success == True:
		print "=="*10
		print "\n%s\t\t téléchargé avec succès dans '%s'\n"%(nom,path)
		zipOK = unzip(path,dest)
		if zipOK == True:
		  print "\n%s\t\t dézippé avec succès dans '%s'\n"%(nom,dest)
		else:
			print "!!"*10
			print "\n%s\t\t échec du dézippage\n"%nom
	else:
		print "!!"*10
		print "%s\t\t échec du téléchargement"%nom
