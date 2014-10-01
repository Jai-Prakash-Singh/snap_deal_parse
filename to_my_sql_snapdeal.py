import glob
import multiprocessing
import time 
import MySQLdb
import ast
from datetime import datetime

pd = "/home/desktop/working_sites/jabong_sub_cat_all2/jabong_sub_cat_all"

num_fetch_threadsm = 5
enclosure_queuem = multiprocessing.JoinableQueue()

def my_strip(x):
    try:
        x = str(x).strip()
        x = MySQLdb.escape_string(x).strip()
    except:
        x = str(x.encode("ascii", "ignore")).strip()
        x = MySQLdb.escape_string(x).strip()

    return x

        


def main(directory, filename):
    db = MySQLdb.connect("localhost","root","6Tresxcvbhy","snapdeal")
    cursor = db.cursor()

    f = open(filename)
    
    for line in f:
        #try:
            line_split = ast.literal_eval(str(line).strip())
            line_split = tuple(map(my_strip, line_split))

            task_id = None

            sql_select = """ select task_id from `snapdeal_data` where `product_url` = "%s" """ %(line_split[11])
            cursor.execute(sql_select)
            results = cursor.fetchone()
        
            if results:   
                task_id = int(results[0])
   
            if task_id:
                sqlentry = """update snapdeal_data set product_desc = "%s", product_spec = "%s", selliing_price = "%s", mrp = "%s", color= "%s", size= "%s", dte= "%s", status= "%s"  where task_id = "%s" """
                sqlentry = sqlentry %(line_split[16], line_split[17], line_split[3], line_split[8] , line_split[9],  line_split[15], line_split[18], line_split[19], task_id)
                result = "updated.................................................................................................................."
        
            else:
                
                sqlentry = """insert into snapdeal_data ( product_id, product_title, target_link, selliing_price, category, sub_category, 
                          brand, image_link, mrp, color, target, product_url, seller, meta_title, meta_desc, size, product_desc, 
                          product_spec, dte, status ) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s",
                          "%s", "%s",  "%s", "%s", "%s", "%s", "%s", "%s", "%s")"""


                print line_split
                print sqlentry
                sqlentry = sqlentry %(line_split) 
                result = "inserted.................................................................................................................."
        
        

            try:
                cursor.execute(sqlentry)
                db.commit()
                print result

            except:
                try:
                    db.ping()
                    cursor.execute(sqlentry)
                    db.commit()
                    print "connection reconnect..................................................................................."
                    print result
                except:
                    db.rollback()
                    print "rollback. ........................................................................................................"
        
        #except:
        #    pass    
        
    db.close()



def main3(i, q):
    for directory,  filename in iter(q.get, None):
        try:
            print filename
            main(directory, filename)
        except:
            pass

        time.sleep(2)
        q.task_done()

    q.task_done()



def supermain(directory):
    flptrn = "%s/*.csv" %(directory)
    csv_file_list = glob.glob(flptrn)
    #print csv_file_list

    procs = []

    for i in range(num_fetch_threadsm):
        procs.append(multiprocessing.Process(name = str(i), target=main3, args=(i, enclosure_queuem,)))
        procs[-1].start()

    for filename in csv_file_list:
        enclosure_queuem.put((directory, filename.strip()))

    enclosure_queuem.join()

    for p in procs:
        enclosure_queuem.put(None)

    enclosure_queuem.join()

    for p in procs:
        p.join(1800)    



if __name__=="__main__":
    tstart = datetime.now()
    directory = "/home/desktop/weekly_sites/snap170514_second_all/snap_deal_dir"
    #supermain(directory)
    filename = "/home/desktop/weekly_sites/snap170514_second_all/snap_deal_dir/Fashion_Accessories.csv"
    main(directory, filename)
    
    tend = datetime.now()
    print tend - tstart

