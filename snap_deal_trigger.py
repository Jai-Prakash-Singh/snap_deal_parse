
def main():

    import sys
    sys.path.append("/home/desktop/weekly_sites/snap170514_second_all/snap_deal_dir")

    import code1_second_snap_deal
    import  code2_first_snapdael
    import  last_page_info_snapdeal
    import code3_first_snapdeal

    directory = "/home/desktop/weekly_sites/snap170514_second_all/snap_deal_dir"


    #code1_second_snap_deal.supermain(directory)

    #code2_first_snapdael.supermain(directory)
    #code3_first_snapdeal.supermain(directory)

    #import mysql_con_python_mirrow
    #mysql_con_python_mirrow.supermain()

    #import to_my_sql_mirrow
    #to_my_sql_mirrow.supermain(directory)

    
    ##import code1_first_fetch_image
    ##code1_first_fetch_image.supermain(directory)

    ##import last_code
    ##last_code.supermain(directory)

    #import mysql_con_python_mirrow2
    #mysql_con_python_mirrow2.supermain()

    #import code6_first_to_cmmn_myntra
    #code6_first_to_cmmn_myntra.supermain()

    import shutil 
    import time 

    directory2 = "%s%s" %(directory, time.strftime("%d%m%y"))
    shutil.move(directory, directory2)



if __name__=="__main__":
    main()
