import phan_proxy
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select
import logging
from bs4 import BeautifulSoup
from lxml import html 


logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')



def ajax_complete(driver):
    try:
        return 0 == driver.execute_script("return jQuery.active")

    except WebDriverException:
        pass



def ajax_call(driver):
    try:
         WebDriverWait(driver, 5).until( ajax_complete,  "Timeout waiting for page to load")

    except WebDriverException:
        pass

    return driver 



def driver_scroller(driver):
    height = 0
    loop = True
    rot = 0

    while (loop is True) and rot < 15:
        logging.debug("scrolling...")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver = ajax_call(driver)  
        #time.sleep(2)

        heightnow = driver.execute_script("return Math.max(document.documentElement.clientHeight, document.body.scrollHeight, document.documentElement.scrollHeight, document.body.offsetHeight, document.documentElement.offsetHeight );")
        driver = ajax_call(driver)

        logging.debug(heightnow)
        #time.sleep(2)

        if heightnow == height:
            loop = False

        else:
            height = heightnow
            loop = True

        rot = rot +  1

    return driver



def sub_scroller(driver, xpth):
    loop = True
    rot2 = 0

    while (loop is True) and rot2 < 20 :
        try:
            logging.debug("clicking......................................................................................................")
            #driver.execute_script("window.scrollBy(0,  -350)", "")
            
            driver.find_element_by_xpath(xpth).click()
            driver = ajax_call(driver)

            #time.sleep(2)
            driver = driver_scroller(driver)

            driver = ajax_call(driver)
            #time.sleep(2)

        except:
            loop = False

        rot2 =  rot2 +  1

    return driver



def main(driver, xpth = None):
    driver = driver_scroller(driver)
 
    if xpth is not  None:
        driver = sub_scroller(driver, xpth)

    return driver 



def supermain():
    link = "http://www.snapdeal.com/products/mens-footwear-sports-shoes/?q=Wearability_s%3AFootball&sort=plrty&#plrty|"
    link ="http://www.snapdeal.com/products/mens-footwear-casual-shoes?q=Price:399,7899&sort=rec"
    driver = phan_proxy.main(link)
        
    try:
         driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div/a/img").click()
         logging.debug("clicked..................................................................")

    except:
        pass
    
    driver = main(driver) 
    page = driver.page_source 

    soup = BeautifulSoup(page, "html.parser")

    item_big_box_list = soup.find("div", attrs={"id":"products-main4"})
    item_box_list = item_big_box_list.find_all("div", attrs={"class":"product_grid_row"})

    for item_box in item_box_list:
        item_sub_box_list  = item_box.find_all("div", attrs={"class":"product_grid_cont gridLayout3"})


        for item_sub_box in item_sub_box_list:
            item_link = item_sub_box.find("a", attrs={"class":"hit-ss-logger somn-track prodLink"}).get("href")
            print item_link

    print len(item_box_list)

    driver.delete_all_cookies()
    driver.quit()



if __name__=="__main__":
    supermain()
        
