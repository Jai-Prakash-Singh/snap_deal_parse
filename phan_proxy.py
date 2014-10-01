import logging
from selenium import webdriver
import logging
from  random  import choice
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s', )



def main(link):
    f2 = open("/home/desktop/proxy_http_auth.txt")
    proxy_list = f2.read().strip().split("\n")
    f2.close()

    for l in xrange(6):
        ip_port = choice(proxy_list).strip()
        logging.debug(ip_port)

        user_pass = ip_port.split("@")[0].strip()
        prox = "--proxy=%s" % (ip_port.split("@")[1].strip())

        service_args = [prox, '--proxy-auth='+user_pass, '--proxy-type=http', '--load-images=no']
        dcap = dict(DesiredCapabilities.PHANTOMJS)

        dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:23.0) Gecko/20100101 Firefox/23.0")
        dcap["--disable-popup-blocking"] = False

        driver = webdriver.PhantomJS(service_args = service_args, desired_capabilities=dcap)
        #driver.start_session(desired_capabilities=dcap)
        #driver.get(link)
        #driver.refresh()
        driver.maximize_window()
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)


            
        try:
            driver.get(link)

        except:
            pass

        if str(driver.current_url).strip() != "about:blank":
            return driver 

        else:
            driver.delete_all_cookies()
            driver.quit()

    return None




if __name__=="__main__":
    link = "http://www.jabong.com/"
    driver = main(link)[-1]
    page = driver.page_source
    print page
                 
