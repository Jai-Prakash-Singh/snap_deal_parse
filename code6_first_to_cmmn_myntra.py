#!/usr/bin/python

import MySQLdb
import os 



class to_common(object):
    
    def __init__(self, dbname, table1, table2, zovtable, zovtable2, sitename, seller_brand, directory, csvfile):
        self.directory = directory 
        self.dbname = dbname
	self.table1  = table1
	self.table2 = table2
	self.seller_brand = seller_brand
        self.csvfile = csvfile
        self.zovtable = zovtable
        self.zovtable2 = zovtable2
        self.sitename= sitename
	changemode = "chown mysql:mysql %s" %(directory)
        os.system(changemode)
	
	   

	db = MySQLdb.connect("192.99.13.229","root","6Tresxcvbhy", dbname)
	cursor = db.cursor()

	self.db = db 
	self.cursor = cursor

        self.db2 = db2 = MySQLdb.connect("54.201.218.138","root","india@123", "zov", local_infile = 1)
        self.cursor2 = cursor2 = db2.cursor()



    def __del__(self):
        self.db.close()
        self.db2.close()



    def table_connect(self):
        cursor = self.cursor
        db = self.db 

        sql = """ truncate %s""" %(self.table2)

        try:
            cursor.execute(sql)
            db.commit()

        except:
            db.rollback()
    

        sql = """insert into %s ( SKU, Title, Link, Price, Category, subCategory, Brand, Image, ListPrice,\
                                  ColourName, targetAudience, productUrl, seller, metaTitle, metaDescription,\
                                  size, log_discription, log_specification, seller_brand\
				) \
	                        ( select product_id, product_title, product_url, selliing_price, category, sub_category, brand\
				  ,sort_image_link, mrp, color, target, product_title_zovon, seller, meta_title, meta_desc, size, \
				  product_desc, product_spec, seller_brand from %s where  upload_status = 'NO'\
                                  and upload_image_status = "YES" \
				  and failing_status = "NO" and  status = "A"\
				)"""
        sql = sql %(self.table2,  self.table1)
        try:
            cursor.execute(sql)
            db.commit()

        except:
            db.rollback()  

        sql = """update %s set upload_status  = "YES" """
        sql = sql %(self.table1)

        try:
            cursor.execute(sql)
            db.commit()

        except:
            db.rollback()



    def to_zovon(self):
        csvfile = self.csvfile
        sql = """ select SKU, Title, Link, Price, Category, subCategory, Brand, Image, ListPrice,\
                  ColourName, targetAudience, productUrl, seller, metaTitle, metaDescription,\
                  size, log_discription, log_specification, seller_brand  from %s  where updated_just_now = "YES" INTO OUTFILE "%s" \
		  FIELDS ENCLOSED BY '"' TERMINATED BY ',' ESCAPED BY '\'
		  LINES TERMINATED BY '\r\r\r\r\n'; """

        sql = sql %(self.table2, self.csvfile)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()



    def to_zovon_import(self):

        sql = """CREATE TEMPORARY TABLE %s LIKE %s;""" %(self.table1, self.zovtable)
        try:
            self.cursor2.execute(sql)
            self.db2.commit()
        except:
            self.db2.rollback()

        
        
        sql = """LOAD DATA local INFILE "%s"  replace   INTO TABLE %s  FIELDS TERMINATED BY ',' ENCLOSED BY '"' \
                 ESCAPED BY '\' LINES TERMINATED BY '\r\r\r\r\n' \
                 ( SKU, Title, Link, Price, Category, subCategory, Brand, Image, ListPrice,\
                   ColourName, targetAudience, productUrl, seller, metaTitle, metaDescription,\
                   size, log_discription, log_specification, seller_brand );"""

        sql = sql %(self.csvfile, self.table1)

        try:
            self.cursor2.execute(sql)
            self.db2.commit()
        except:
            self.db2.rollback()

        table_match = {"your_table":self.zovtable, "your_temp_table":self.table1}

        sql = """insert into %(your_table)s ( SKU, Title, Link, Price, Category, subCategory, Brand, Image, ListPrice,\
                                  ColourName, targetAudience, productUrl, seller, metaTitle, metaDescription,\
                                  size, log_discription, log_specification, seller_brand\
                                ) \
                                ( select SKU, Title, Link, Price, Category, subCategory, Brand, Image, ListPrice,\
                                  ColourName, targetAudience, productUrl, seller, metaTitle, metaDescription,\
                                  size, log_discription, log_specification, seller_brand from %(your_temp_table)s
                                ) ON DUPLICATE KEY """
        sql = sql %(table_match)


 
        sql2 = """UPDATE \
               Price = %(your_temp_table)s.Price, \
               ListPrice = %(your_temp_table)s.ListPrice,\
               ColourName = %(your_temp_table)s.ColourName,\
               size = %(your_temp_table)s.size,\
               log_discription = %(your_temp_table)s.log_discription, \
               log_specification = %(your_temp_table)s.log_specification,\
               p_status ="NU"; """ %(table_match)

        sql = """%s%s""" %(sql, sql2)


        try:
            self.cursor2.execute(sql)
            self.db2.commit()
        except:
            self.db2.rollback()

        sql ="DROP TEMPORARY TABLE %(your_temp_table)s;" %(table_match)

        try:
            self.cursor2.execute(sql)
            self.db2.commit()
        except:
            self.db2.rollback()



    def pattern_matching(self):

        #sql = """SELECT target, category, sub_category, sub_category from %s WHERE upload_status = 'YES'\
        #                          and upload_image_status = "YES" \
        #                          and failing_status = "NO" and  status = "A" """

        #sql = sql %(self.table1)

        #self.cursor.execute(sql)
        #results2 = self.cursor.fetchall()

        #t_c_s_ssc_ptrn = ["+".join(list(t_c_s_ssc)) for t_c_s_ssc in results2]

        sql = """SELECT other_cat, zov_cat  FROM %s  WHERE site_name = "%s" and site_table = "%s" """ 
        sql = sql %(self.zovtable2, self.sitename, self.table1)

        self.cursor2.execute(sql)
        results = self.cursor2.fetchall()
         

        pattern_matching2 = self.pattern_matching2
        table2, table1 = self.table2, self.table1
        cursor, db = self.cursor, self.db

        pattern_dict = {}

        for ptrn in results:
            pattern_dict[ptrn[0]] = ptrn[1] 

        self.pattern_dict = pattern_dict


        info = [pattern_matching2(prtnset[0], prtnset[1], table2, table1, cursor, db ) for prtnset in results]

        del info[:]
        del info  




    def pattern_matching2(self, k, v, table2, table1, cursor, db):
        main_ptrn = [ln.strip() for ln in k.split("+")]
        subs_ptrn = [ln.strip().lower() for ln in v.split("+")]

        length = len(subs_ptrn)
        
        if length == 4:
	    return 0

	elif length == 3:
            pass

	elif length == 2:
	    subs_ptrn.extend([" "])

	elif length == 1:
	    subs_ptrn.extend([" ", " "])

        else:
            return 0

	subs_ptrn.extend(main_ptrn)

        final_string = [table2, table1]
        final_string.extend(subs_ptrn)
        final_string = tuple(final_string)

        sql = """UPDATE %s t2 INNER JOIN %s t1 \
                 ON t1.product_url = t2.Link \
                 set t2.targetAudience = "%s", t2.Category = "%s", t2.subCategory = "%s" , t2.updated_just_now ="YES"\
		 where t1.target = "%s" and t1.category="%s" and  t1.sub_category="%s" and  t1.ss_category ="%s"; """
 

        sql = sql %(final_string)

        try:
	   cursor.execute(sql)
           db.commit()
           print "updated................................."
	except:
	    db.rollback()

        


    



def supermain():
    import time 
    dbname, table1, table2, seller_brand = ("snapdeal", "snapdeal_data", "snapdeal_data_cmn", "www.snapdeal.com")
    directory = "/home/desktop/weekly_sites/snap170514_second_all/snap_deal_dir"
    csvfile = "%s/to_zovon%s.csv" %(directory, time.strftime("%d%m%y%H%M%S"))
    zovtable = "zovondetails"
    zovtable2 = "site_synonyms"
    sitename = "snapdeal"
    obj = to_common(dbname, table1, table2, zovtable, zovtable2, sitename,  seller_brand, directory, csvfile)
    
    
    obj.table_connect()
    obj.pattern_matching()

    obj.to_zovon()
    obj.to_zovon_import()




    

    




if __name__=="__main__":
    supermain()
     
