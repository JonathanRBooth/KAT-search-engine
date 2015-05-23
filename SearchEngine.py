#KAT Torrent Search Engine

import requests
from bs4 import BeautifulSoup
import time
import os
import sys

filetype = ""
category = ""

print "Welcome to the KickAssTorrents Simple Search Engine!\n\n"

search = raw_input("Insert search term: ")
filetypeselect = raw_input("\nWould you like to filter by file type? yes/no: ")
if filetypeselect == "yes":
    filetype = raw_input("\nWhich file type would you like to filter for?: \n Movies \n TV \n Music \n Books \n Games \n Apps \n XXX \n\n")
    category = "%20category:"

outputpath = raw_input("\n\nWhat would you like the savefile.txt to be named?: ") +".txt"
    
def pages():
    url = "https://kat.cr/usearch/%s%s%s" %(search, category, filetype)
    print "\n The url is: ", url, "\n"
    page = requests.get(url).content
    textblock = BeautifulSoup(page)
    textblock = textblock.find("div").h2
    textblock = textblock.find("span")
    textblock = str(textblock)
    textblock = textblock.replace("<span>  results 1-25 from ","")
    textblock = textblock.replace("</span>","")

    torrentamount = int(textblock)
    pageamount = (torrentamount/25)
    return pageamount

try:   
    pagenumber = pages()
    print "\n", pagenumber + 1, "pages to scrape\n "


    for x in range(0, pagenumber + 1):
        
        url = "https://kat.cr/usearch/%s%s%s/%s" %(search, category, filetype, x)
        print "\n Scraping page:", x, "\n"
        page = requests.get(url).content
        soup = BeautifulSoup(page)

        for link in soup.findAll("a",{"class":"cellMainLink"}): 
            link = link.get('href')
            link = link.encode("ascii","ignore")
            link = link.replace("-"," ")
            link = link.replace("/","")
            link = link.capitalize()
            link = link[:-14]

            savefile = open(outputpath,"a")
            savefile.write(link)
            savefile.write("\n\n")
            savefile.close()

    print "\n All files found"

    
except ValueError:
    print "No results found for search term"

raw_input()