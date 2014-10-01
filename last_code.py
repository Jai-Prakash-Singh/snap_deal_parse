import MySQLdb
import os 
import fileinput
import ast 
import shutil 

class data_base_connect(object):
    def __init__(self, host1, user1, pass1, database1, table1, directory, file_list = []):
        self.host1 = host1
	self.user1 = user1
	self.pass1 = pass1
	self.database1 = database1
        self.file_list = file_list
	self.table1 = table1
	self.directory = directory

        self.db1 = db1 = MySQLdb.connect(host1, user1, pass1, database1)
	self.cursor1 = cursor1 = db1.cursor()


    def __del__(self):
        self.db1.close()



    def readfilelist(self):
        file_list = self.file_list
        directory = self.directory
	table1 = self.table1
	db1 = self.db1
	cursor1 = self.cursor1
        ast_lit = ast.literal_eval

        open_file_object_list = [os.path.join(directory, filename) for filename in file_list]

	tuple_sku = ["'%s'" %(ast_lit(line)[0]) for line  in fileinput.input(open_file_object_list)]
        fileinput.close()
  
        sql = """update %s set upload_image_status = "YES" where product_id in (%s)""" %(table1, ", ".join(tuple_sku))

        #print sql
        #try:
        cursor1.execute(sql)
        db1.commit()
        print "updated........................."
        #except:
        #    db1.rollback()

        del open_file_object_list[:]
        del open_file_object_list
        del tuple_sku[:]
        del tuple_sku

        #[shutil.rmtree(fnm) for fnm in open_file_object_list]


def supermain(directory):
    directory = "%s/image_folder" %(directory)
    host1 = "localhost"
    user1 = "root"
    pass1 = "6Tresxcvbhy"
    database1 = "snapdeal"
    table1  = "snapdeal_data"
    file_list = ["image_folder1/img_transfer.txt", "image_folder2/img_transfer.txt", 
                 "image_folder3/img_transfer.txt", "image_folder4/img_transfer.txt", 
                 "image_folder5/img_transfer.txt"]

    directory = "/home/desktop/weekly_sites/snap170514_second_all/extra_code/"
    
    obj = data_base_connect(host1, user1, pass1, database1, table1, directory, file_list )
    obj.readfilelist()



if __name__=="__main__":
    supermain()


