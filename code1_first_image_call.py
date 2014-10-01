
import req_proxy
from bs4 import BeautifulSoup
from lxml import html
import re
import time
import logging
import sys
import ast
import urllib
import urllib2
import os
import boto
from boto.s3.key import Key
import shutil


def to_cdn(filename, keyname):
    #boto.set_stream_logger('boto')
    c = boto.connect_s3()
    b = c.get_bucket("zovon")
    k = Key(b)
    k.key = "prod_img/%s" %(keyname)
    k.set_metadata("Content-Type", 'image/jpeg')
    k.set_contents_from_filename(filename)
    k.make_public()
    c.close()
    os.remove(filename)




def main(directory, line):
    transfer_direc = "%s/img_not_transfer.txt" %(directory)
    transfer = "%s/img_transfer.txt" %(directory)
    try:
        task_id = line[0]
        link = str(line[-1]).strip()
        page= req_proxy.main(link)
    
        #start = link.rfind("?")
        end= link.rfind("/")
        name =  link[end+1:]
    
        filename = "%s/%s" %(directory,name)
        f = open(filename,'wb')
        f.write(page)
        f.close()

        filename = str(filename).strip()
        keyname = filter(None, filename.split("/"))[-1]
        to_cdn(filename, keyname)

        f = open(transfer, "a+")
        f.write(str(line) + "\n")
        f.close()
    except:
        f = open(transfer_direc, "a+")
        f.write(str(line) + "\n")
        f.close()


    

    
       

if __name__=="__main__":
    line = ("1", "http://assets2.mirraw.com/images/329254/TSPE807_large.jpg?1398074808")
    directory = "/home/desktop/weekly_sites/snap170514_second_all/snap_deal_dir" 
    try:
        os.makedirs(directory)
    except:
        pass
    main(directory, line)
