import req_proxy
from bs4 import BeautifulSoup
from lxml import html 
import phan_scroller
import phan_proxy 
from urlparse import urlparse
import os 
import time 
import sys 
import logging
import re
import multiprocessing

num_fetch_pros = 15
enclosure_queuem = multiprocessing.JoinableQueue()

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s', )



def my_strip(x):
    try:
        x = str(x).replace("\n","").replace("\r","").replace("\t","").replace(",","").strip()

    except:
        x = str(x.encode("ascii", "ignore")).replace("\n","").replace("\r","").replace("\t","").replace(",","").strip()

    return x



def main(directory, link):
    page = req_proxy.main(link)
    #driver = phan_proxy.main(link)

    #try:
    #     driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div/a/img").click()
    #     logging.debug("clicked..................................................................")

    #except:
    #    pass

    #driver = phan_scroller.main(driver)
    #page = driver.page_source

    soup = BeautifulSoup(page, "html.parser")

    target_cat_list = soup.find("div", attrs={"id":"breadCrumbWrapper"}).find_all("span", attrs={"itemprop":"title"})
    filename = "%s/%s.doc" %(directory, "_".join(str(target_cat_list[-1].get_text()).split()))

    f = open(filename, "a+")
    
    item_big_box_list = soup.find("div", attrs={"id":re.compile("products-main")})


    item_box_list = item_big_box_list.find_all("div", attrs={"class":"product_grid_row"})

    for item_box in item_box_list:
        item_sub_box_list  = item_box.find_all("div", attrs={"class":"product_grid_cont gridLayout3"})

        if len(item_sub_box_list) == 0:
            item_sub_box_list  = item_box.find_all("div", attrs={"class":"product_grid_cont gridLayout4"})
        
        for item_sub_box in item_sub_box_list:
            item_link = item_sub_box.find("a", attrs={"class":"hit-ss-logger somn-track prodLink"}).get("href")
            parsed = urlparse(item_link)

            if len(parsed.netloc) == 0:
                item_link = "http://www.snapdeal.com%s" %(item_link)

            size = []
            size_box_list = item_sub_box.find("div", attrs={"class":"productAttr"})
            
            if size_box_list is not None:
                size_option_box = size_box_list.find_all("option")

                for size_option in size_option_box:
                    size.append(size_option.get("value"))

            if len(size) !=0:
                size = filter(None, map(my_strip, size))
    
            info = [link, item_link, size]
            info2 = map(my_strip, info)

            f.write(str(info2) + "\n")
            logging.debug("inserted........................................................................")


    f.close()

    #driver.delete_all_cookies()
    #driver.quit()



def mainpros(i, q):
    for directory, link in iter(q.get, None):
        try:
            link  = link.strip()
            main(directory, link)
            logging.debug(link)

        except:
             eror_file = "%s/code2_first_error_snapdael.txt" %(directory)

             f = open(eror_file, "a+")
             f.write(link.strip() +"\n")
             f.close()

        time.sleep(2)
        q.task_done()

    q.task_done()



def supermain(directory):
    filename = "%s/sub_cat_brand_link_collection.txt" %(directory)

    f = open(filename)

    procs = []

    for i in range(num_fetch_pros):
        procs.append(multiprocessing.Process(target=mainpros, args=(i, enclosure_queuem,)))
        procs[-1].start()

    for  link in f:
        enclosure_queuem.put((directory, link))

    enclosure_queuem.join()

    for p in procs:
        enclosure_queuem.put(None)

    enclosure_queuem.join()

    for p in procs:
        p.join(180)

    f.close()

    print "Done............"



if __name__=="__main__":
    directory = "/home/desktop/weekly_sites/snap170514_second_all/snap_deal_dir"

    try:
        os.makedirs(directory)

    except:
        pass


    #supermain(directory)

    link = "http://www.snapdeal.com/products/home-kitchen-home-decoratives/?q=Brand:oocc"
    main(directory, link)

    




