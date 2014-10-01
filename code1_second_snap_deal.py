from bs4 import BeautifulSoup
from lxml import html 
import logging
import os 
import time 
from urlparse import urlparse
import req_proxy
import time
from Queue import Queue
from threading import Thread
import re 

num_fetch_threads2 = 20
enclosure_queue2 = Queue()

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s', )


def my_strip(x):
    try:
        x = str(x).strip()
    except:
        x = str(x.encode("ascii", "ignore")).strip()

    return x 




def cat_to_subcat_brand(fb, link):
    page = req_proxy.main(link)

    soup = BeautifulSoup(page, "html.parser")
    brand_big_box = soup.find("div", attrs={"name":"Brand"})

    brand_box_list = brand_big_box.find_all("input", attrs={"filtername":"Brand"})

    for brandbox in brand_box_list:
        brand = my_strip(brandbox.get("value"))
        #print "http://www.snapdeal.com/products/men-apparel-jeans/?q=Brand%3A"+ brand + "&FID=checkbox_searchable_Brand%20%3A" + brand
        brand_link =  "%s/?q=Brand:%s" %(link, brand)
        fb.write(brand_link + "\n")
        logging.debug("inserted...................................................................................")
        


def mainthread3(i, q):
    for directory, f2, link in iter(q.get, None):
        try:
            link = link.strip()
            cat_to_subcat_brand(f2, link)

        except:
            filename = "%s/code1_second_brand_error_snap_deal.txt" %(directory)
            f3 = open(filename, "a+")
            f3.write(link.strip() + "\n")
            f3.close()

            logging.debug("error...........................................................................")

        time.sleep(2)
        q.task_done()

    q.task_done()



def main3( directory, filename):
    filename = "%s/sub_cat_link_collection.txt" %(directory)
    filename2 = "%s/sub_cat_brand_link_collection.txt" %(directory)

    f = open(filename)
    f2 = open(filename2, "a+")

    procs = []

    for i in range(num_fetch_threads2):
        procs.append(Thread(target=mainthread3, args=(i, enclosure_queue2,)))
        procs[-1].start()

    for link in f:
        enclosure_queue2.put((directory, f2, link))

    print '*** Main thread waiting'
    enclosure_queue2.join()
    print '*** Done'

    for p in procs:
        enclosure_queue2.put(None)

    enclosure_queue2.join()

    for p in procs:
        p.join(180)

    f2.close()
    f.close()





def cat_to_subcat(fs, link):
    page = req_proxy.main(link)

    soup = BeautifulSoup(page, "html.parser")
    cat_big_box = soup.find("div", attrs={"id":"matchingCatbox"})

    cat_box_list = cat_big_box.find_all("a", attrs={"class":re.compile("somn-track")})

    for  cat_box in cat_box_list:
        cat_link = my_strip(cat_box.get("href"))
        
        fs.write(cat_link + "\n")



def mainthread2(i, q):
    for directory, f2, link in iter(q.get, None):
        try:
            link = link.strip()
            cat_to_subcat(f2, link)

        except:
            filename = "%s/code1_second_error_snap_deal.txt" %(directory)
            f3 = open(filename, "a+")
            f3.write(link.strip() + "\n")
            f3.close()

            logging.debug("error...........................................................................")

        time.sleep(2)
        q.task_done()

    q.task_done()



def main2(directory, filename):
    filename2 = "%s/sub_cat_link_collection.txt" %(directory)

    f = open(filename)
    f2 = open(filename2, "a+")

    procs = []

    for i in range(num_fetch_threads2):
        procs.append(Thread(target=mainthread2, args=(i, enclosure_queue2,)))
        procs[-1].start()

    for link in f:
        enclosure_queue2.put((directory, f2, link))

    print '*** Main thread waiting'
    enclosure_queue2.join()
    print '*** Done'

    for p in procs:
        enclosure_queue2.put(None)

    enclosure_queue2.join()

    for p in procs:
        p.join(180)

    f2.close()
    f.close()



def main(directory, mainlink):
    filename = "%s/complete_link_collection.txt" %(directory)

    f = open(filename, "a+")

    page = req_proxy.main(mainlink)

    soup = BeautifulSoup(page, "html.parser")
    cat_collection_box = soup.find("div", attrs={"class":"brw_bdr"})
    
    link_list = cat_collection_box.find_all("a")

    for link in link_list:
        link  = link.get("href")

        parsed = urlparse(link)

        if len(parsed.netloc) == 0:
            link = "http://www.snapdeal.com%s" %(link)
            
        f.write(str(link) + "\n")
        #print link

    f.close()
    
    return filename



def supermain(directory):

    try:
        os.makedirs(directory)

    except:
        pass

    link = "http://www.snapdeal.com/offers/wa-resolution"
    filename = main(directory, link)
    
    main2( directory, filename)

    main3(directory, filename)

    return directory


if __name__=="__main__":
    directory = "/home/desktop/weekly_sites/snap170514_second_all/snap_deal_dir"
    supermain(directory)

    #link = "http://www.snapdeal.com/products/mens-footwear"
    #f = open("sub_cat_brand_collection.txt", "a+")
    #link = "http://www.snapdeal.com/products/bags"
    #cat_to_subcat_brand(f, link)
    
    #f.close()

    #filename = "sub_cat_link_collection.txt"    
    #f = open(filename, "a+")
    #main3(directory, filename)
    #cat_to_subcat(f, "http://www.snapdeal.com/products/mobiles-mobile-phones")
    #f.close()
