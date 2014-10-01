import multiprocessing
import logging 
import glob
import time 
from Queue import Queue
from threading import Thread
import last_page_info_snapdeal

num_fetch_threads2 = 5
enclosure_queue2 = Queue()

num_fetch_pros = 10
enclosure_queuem = multiprocessing.JoinableQueue()

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s', )



def mainthread2(i, q):
    for directory, f2, line in iter(q.get, None):
        try:
            last_page_info_snapdeal.main(f2, line)

        except:
            fname = "%s/code3_first_error_snapdeal.txt" %(directory)
            f3 = open(fname, "a+")
            f3.write(line.strip() + "\n")
            f3.close()

            logging.debug("error...........................................................................")

        time.sleep(2)
        q.task_done()

    q.task_done()



def main(directory, filename):
    filename2 = "%s.csv" %(filename[:-4])

    f = open(filename)
    f2 = open(filename2, "a+")

    
    procs = []

    for i in range(num_fetch_threads2):
        procs.append(Thread(target=mainthread2, args=(i, enclosure_queue2,)))
        procs[-1].start()

    for line in f:
        enclosure_queue2.put((directory, f2, line))

    print '*** Main thread waiting'
    enclosure_queue2.join()
    print '*** Done'

    for p in procs:
        enclosure_queue2.put(None)

    enclosure_queue2.join()

    for p in procs:
        p.join(180)

    f2.close()
    f.close()    



def mainpros(i, q):
    for directory, filename in iter(q.get, None):
        main(directory, filename)
        time.sleep(2)
        q.task_done()

    q.task_done()



def supermain(directory):
    filepattern = "%s/*.doc" %(directory)

    doc_file_list = glob.glob(filepattern)
    procs = []

    for i in range(num_fetch_pros):
        procs.append(multiprocessing.Process(target=mainpros, args=(i, enclosure_queuem,)))
        procs[-1].start()

    for filename in doc_file_list:
        enclosure_queuem.put((directory, filename))

    enclosure_queuem.join()

    for p in procs:
        enclosure_queuem.put(None)

    enclosure_queuem.join()

    for p in procs:
        p.join(3600)

    print "Done............"



if __name__=="__main__":
    directory = "/home/desktop/weekly_sites/snap170514_second_all/snap_deal_dir"

    #supermain(directory)

    filename = "/home/desktop/weekly_sites/snap170514_second_all/snap_deal_dir/Watches.doc"
    main(directory, filename)    
