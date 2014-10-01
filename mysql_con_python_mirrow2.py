#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb



def supermain():
    db = MySQLdb.connect("localhost","root","######")
    cursor = db.cursor()

    sql = "create database if not exists  snapdeal"
    cursor.execute(sql)

    sql = "use snapdeal"
    cursor.execute(sql)
    

    sql = """create table IF NOT EXISTS  snapdeal_data_cmn (
               detailId int(11) NOT NULL AUTO_INCREMENT,
               zovon_temp_id varchar(100),
	       SKU varchar(255),
               Title varchar(255), 
	       Link varchar(300),
	       Price varchar(255),
	       Category varchar(300), 
               subCategory varchar(300), 
               Brand varchar(300), 
               Image varchar(300), 
	       ListPrice varchar(255), 
	       ColourName varchar(300), 
               targetAudience varchar(300), 
	       productUrl varchar(255), 
	       seller varchar(255), 
	       metaTitle varchar(255), 
	       metaDescription varchar(255), 
	       meta_keyword varchar(255), 
	       brand_image varchar(255), 
	       seller_brand varchar(255), 
	       size varchar(255), 
	       log_discription  varchar(255),
	       log_specification varchar(255),
	       display_ord int(11),
	       l_status enum('A', 'IA') DEFAULT 'A',
               p_status enum('N', 'U') DEFAULT 'N',
               primary key (detailId)
	    )"""

    cursor.execute(sql)

    try:
        sql2 = "create unique index snapdeal_data_cmn_index on snapdeal_data_cmn (Link)"
        cursor.execute(sql2)
        db.commit()   
    except:
        pass

    try:
        sql2 = "create  index snapdeal_data_cmn_index2 on snapdeal_data_cmn \
               (zovon_temp_id, SKU, Title, Category, subCategory, Image, targetAudience,  productUrl, l_status, p_status )"
        cursor.execute(sql2)
        db.commit()
    except:
        pass


    sql = """alter ignore  table  snapdeal_data_cmn  add   updated_just_now  enum('NO','YES', 'F') DEFAULT 'NO';""" 

    try:
        cursor.execute(sql)
        db.commit()
    except:
        pass



    db.close()
    print " db_close()......................................................"



    



if __name__=="__main__":
    supermain()

