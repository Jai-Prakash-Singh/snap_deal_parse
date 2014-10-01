from bs4 import BeautifulSoup
from lxml import html 
import phan_proxy
import logging
import os 
import time 
from urlparse import urlparse

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s', )



def main(directory, mainlink):
    filename = "%s/complete_link_collection.txt" %(directory)

    f = open(filename, "a+")

    driver = phan_proxy.main(mainlink)
   
    try:
         driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div/a/img").click()
         logging.debug("clicked..................................................................")

    except:
        pass

    page = driver.page_source
    driver.delete_all_cookies()
    driver.quit()
 
    soup = BeautifulSoup(page, "html.parser")
    link_list = soup.find_all("a", attrs={"class":"somn-track"})

    for link in link_list:
        link  = link.get("href")

        parsed = urlparse(link)

        if len(parsed.netloc) == 0:
            link = "http://www.snapdeal.com%s" %(link)
            
        f.write(str(link) + "\n")
        print link

    f.close()



def supermain(directory):
    

    try:
        os.makedirs(directory)

    except:
        pass

    link = "http://www.snapdeal.com"
    main(directory, link)

    return directory



if __name__=="__main__":
    directory = supermain()

