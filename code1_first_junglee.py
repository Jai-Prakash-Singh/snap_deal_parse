import req_proxy
from bs4 import BeautifulSoup
from lxml import html 
import re 
import os 
import multiprocessing
import time 
import ast
import sys 
#import last_page_info_junglee

from Queue import Queue
from threading import Thread
import re

#num_fetch_threads2 = 20
#enclosure_queue2 = Queue()


#num_fetch_pros = 30
#enclosure_queuem = multiprocessing.JoinableQueue()

num_fetch_pros = 15
enclosure_queuem = Queue()




class home_page_yabhi(object):
    def __init__(self, directory, link):
        self.link  = link
	self.directory = directory

	try:
            os.makedirs(directory)
	except:
	    pass

	self.filename = "%s/ct_cl_sct_scl_ssct_sscl.txt" %(directory)   
	self.filobj = open(self.filename, "a+")


        self.filename_sc_scl_br_bl = "%s/ct_cl_sct_scl_ssct_sscl_br_bl.txt" %(directory)
        self.brfilobj = open(self.filename_sc_scl_br_bl, "a+")


        self.filename_pr_pl = "%s/ct_cl_sct_scl_ssct_sscl_br_bl_pl.txt" %(directory)
        self.pr_pl_filobj =  open(self.filename_pr_pl, "a+")


        self.filename_pr_info = "%s/ct_cl_sct_scl_ssct_sscl_br_bl_pl_info.txt" %(directory)
        self.pr_pl_info_filobj =  open(self.filename_pr_info, "a+")

        self.filename_pr_pl_info2 = "%s/ct_cl_sct_scl_ssct_sscl_br_bl_pl_info2.txt" %(directory)
        self.pr_pl_info2_filobj =  open(self.filename_pr_pl_info2, "a+")



    def my_strip(self, x):
        try:
	    x = str(x).strip()

	except:
	    x = str(x.encode("ascii", "ignore")).strip()

	return x 




    def __del__(self):
	del self.link
	self.filobj.close()
        self.brfilobj.close()
        self.pr_pl_filobj.close()
        self.pr_pl_info_filobj.close()
        self.pr_pl_info2_filobj.close()



    def cat_sct_lnk_fm_link(self):
        """given a link extract cat sub subcatlink"""

        link = self.link
        page = req_proxy.main(link)
        soup = BeautifulSoup(page, "html.parser")

        my_strip = self.my_strip
        ct_sub_sublink = self.ct_sub_sublink = []

        for tagt in ["Clothing", "Shoes", "Watches", "Bags & Accessories", "Jewellery", "Beauty"]:
            beauti_tag = soup.find("a", text=tagt).find_parent("div", attrs={"class":"directory-column"})
            beauti_tag_list  = beauti_tag.find("div", attrs={"class":"category"}).find_all("a")

            ct_sub_sublink.extend([   map(my_strip, [tagt, beauti_tag.get_text(), "http://www.junglee.com%s" %(beauti_tag.get("href"))])
                                  for beauti_tag in beauti_tag_list
                              ])



    def sscat_sslink(self, line):
        """ given a  ct sct scl  find subsubcate subcatelink"""
        link = line[-1]

        page = req_proxy.main(link)
	soup = BeautifulSoup(page, "html.parser")
     
        ct_sct_scl_ssc_ssl = soup.find("strong", text=re.compile(line[-2])).find_parent("li")
        ct_sct_scl_ssc_ssl = ct_sct_scl_ssc_ssl.find_next_siblings("li", attrs={"style":"margin-left: 6px"})

        filobj_write = self.filobj.write
	my_strip = self.my_strip 

	info = [ filobj_write(str(map(my_strip, line + [ ct_sct_scl_ssc_ssl_box.get_text(), ct_sct_scl_ssc_ssl_box.a.get("href") ])) + "\n")
	         for ct_sct_scl_ssc_ssl_box in  ct_sct_scl_ssc_ssl
	       ]

	del info[:]
	del info



    def sscat_sslink_br_bl(self, line):
  
        """ given a  ct sct scl  subsubcate subcatelink find br and brl"""
	line = ast.literal_eval(line)
        link = "http://www.junglee.com%s" %(line[-1])

        line[-1] = link

        page = req_proxy.main(link)
        soup = BeautifulSoup(page, "html.parser")

        brand_main_div = soup.find("h2", text=re.compile("Brand")).find_next("ul")
        brand_main_div = brand_main_div.find_all("a")

        filobj_write = self.brfilobj.write
        my_strip = self.my_strip

        info = [ filobj_write(str(map(my_strip, line + [ brand_div_box.get_text(), brand_div_box.get("href") ])) + "\n")
                 for brand_div_box in  brand_main_div
               ]

        del info[:]
        del info



    def get_product(self, line):

        """ given a  ct sct scl  subsubcate subcatelink br and brl find product"""
        line = ast.literal_eval(line)
        link = "http://www.junglee.com%s" %(line[-1])

        line[-1] = link
        
        page = req_proxy.main(link)
        soup = BeautifulSoup(page, "html.parser")

        pro_div_list = soup.find_all("div", attrs={"id":re.compile(r"^result_[\d]{1,}$")})

        filobj_write = self.pr_pl_filobj.write
        my_strip = self.my_strip

        info = [ filobj_write(str(  map(  my_strip, 
                                          line + [ pro_div.find("img", attrs={"alt":"Product Details"}).find_parent("a").get("href") ]
                                       )
                                 ) 
                                 + "\n"
                             )
                 for pro_div  in  pro_div_list
               ]

        del info[:]
        del info



    def get_pro_info(self, line):
        
        last_page_info_junglee.main(self.pr_pl_info_filobj ,self.pr_pl_info2_filobj , line)  

          

    def que_thread(self, taget_fun, rotate_obj, find_subcat):
        self.procs = procs =  []

        for i in range(num_fetch_pros):
	    #procs.append(multiprocessing.Process(target = taget_fun, args=(i, enclosure_queuem, find_subcat)))
            procs.append(Thread(target=taget_fun,  args=(i, enclosure_queuem, find_subcat)))
	    procs[-1].start()

        for line in rotate_obj:
            enclosure_queuem.put(line)

        enclosure_queuem.join()

        for p in procs:
            enclosure_queuem.put(None)

        enclosure_queuem.join()

        for p in procs:
            p.join(1800)



    def testing_output(self, i, q, find_subcat):
        for  line in iter(q.get, None):

            try:
	        find_subcat(line)
            except:
                pass

	    time.sleep(2)
	    q.task_done()
        q.task_done()



        
def supermain(directory):
    link = "http://www.junglee.com/site-directory/ref=footer_menu_all"
    
    obj = home_page_yabhi(directory, link)
    obj.cat_sct_lnk_fm_link()
    obj.que_thread(obj.testing_output, obj.ct_sub_sublink, obj.sscat_sslink)
    
    f = open(obj.filename)
    obj.que_thread(obj.testing_output, f, obj.sscat_sslink_br_bl)
    f.close()

    f = open(obj.filename_sc_scl_br_bl)
    obj.que_thread(obj.testing_output, f, obj.get_product)
    f.close()

    f = open(obj.filename_pr_pl)
    obj.que_thread(obj.testing_output, f, obj.get_pro_info)
    f.close()
   
   
  



if __name__=="__main__":
    directory = "/home/desktop/working_sites/junglee/junglee_dir"
    supermain(directory)
        
