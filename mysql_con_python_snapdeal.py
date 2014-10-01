#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb



def supermain():
    db = MySQLdb.connect("localhost","root","xxxxxxxxx")
    cursor = db.cursor()

    sql = "create database if not exists  snapdeal"
    cursor.execute(sql)

    sql = "use  snapdeal"
    cursor.execute(sql)
    
    #dte TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    sql = """create table IF NOT EXISTS  snapdeal_data (
               task_id int(11) NOT NULL AUTO_INCREMENT,
               product_id varchar(100),
	       product_title text ,
	       target_link text,
	       selliing_price text,
	       category text, 
	       sub_category text, 
	       brand text, 
	       image_link text, 
	       mrp text, 
	       color text, 
	       target text, 
	       product_url varchar(500), 
	       seller text, 
	       meta_title text, 
	       meta_desc text, 
	       size text, 
	       product_desc  text,
	       product_spec text,
	       dte text,
	       status varchar(10),
               primary key (task_id)
	    )"""

    cursor.execute(sql)

    try:
        sql2 = "create unique index snapdeal_index on snapdeal_data (product_url , status )"
        cursor.execute(sql2)  
    except:
        pass
  
    db.close()
    print " db_close()......................................................"



if __name__=="__main__":
    supermain()

