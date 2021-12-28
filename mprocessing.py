from multiprocessing import Process
import concurrent.futures
import time

def do_something():
    print('Sleeping 1 second...')
    time.sleep(1)
    print('Done sleeping...')


def do_something_with_args(seconds):
    print(f'Sleeping {seconds} second(s)...')
    time.sleep(seconds)
    feedback= 'Done sleeping..'
    print(feedback)


def do_something_with_args_no_printing(seconds):
    print(f'Sleeping {seconds} second(s)...')
    time.sleep(seconds)
    return 'Done sleeping...'




if __name__ == '__main__':
    #to get more accurate results the perf_counter_ns() function can be used to get the time in nanoseconds.
    start= time.perf_counter()
    #run the two processes one after another(the non-multiprocessing way)
    do_something()
    do_something()
    finish= time.perf_counter()
    time_taken= round(finish-start,2)

    assert time_taken>2,"The two processes should take more than 2 seconds."


    print(f' Finished in {time_taken} seconds')



    start= time.perf_counter()
    #run the two processes concurrently (the multiprocessing way) for just two processes.
    p1= Process(target=do_something)
    p2= Process(target=do_something)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    finish= time.perf_counter()

    time_taken= round(finish-start,2)

    assert time_taken< 2,"The two processes should take less than 2 seconds."

    print(f' Finished in {time_taken} seconds')



    start= time.perf_counter()

    processes= []
    #run the two processes concurrently (the multiprocessing way) for many processes.
    for _ in range(10):
         p= Process(target=do_something)
         p.start()
         #the join. can not be called here since all the process need to be started
         #before any of them is joined. The process will be stored in a list  in which all 
         #of them will be joined
         processes.append(p)

    for p in processes:
        p.join()
        
    finish= time.perf_counter()

    time_taken= round(finish-start,2)

    #in this case it does not mean that the processor has 10 cores. The os provides ways to 
    #switch task for the idle cores.
    assert time_taken< 2,"The two processes should take less than 2 seconds."
    print(f' Finished in {time_taken} seconds')



    start= time.perf_counter()

    processes= []
    seconds=1.5
    #run the two processes concurrently (the multiprocessing way) for many processes.
    for _ in range(10):
         p= Process(target=do_something_with_args, args=[seconds])
         p.start()
         #the join. can not be called here since all the process need to be started
         #before any of them is joined. The process will be stored in a list  in which all 
         #of them will be joined
         processes.append(p)

    for p in processes:
        p.join()
        
    finish= time.perf_counter()

    time_taken= round(finish-start,2)

     #give 1 second for context switching and other processes.
    assert time_taken< seconds+1,f"The two processes should take less than {seconds+1}seconds."
    print(f' Finished in {time_taken} seconds')


   #the ideal way of handling mutitprocessing
    start= time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        #return a future object that will be excuted.
         secs=[5,4, 3, 2,1 ]
         results= [executor.submit(do_something_with_args_no_printing, sec) for sec in secs]
         for f in concurrent.futures.as_completed(results):
          print(f.result())
    finish= time.perf_counter() 
    time_taken= round(finish-start,2)


    print(f' Finished in {time_taken} seconds')
    assert time_taken< 5+1,f"The processes should take less than {seconds+1}seconds."




   #using the buildin map function that call  the passed function 
   #with each item that is passed in the iterable.
    start= time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor()   as executor:
   
         secs=[5,4, 3, 2,1 ]

         #return  the result of the function with the order of which the 
         #the process were started.
         results= executor.map(do_something_with_args_no_printing,secs)
        #  for result in results:
        #      #For any execeptions that will be thrown in the multiprocessing ,
        #      #they should be caught in the iterator.
        #      print(result)
    finish= time.perf_counter() 
    time_taken= round(finish-start,2)

 
    print(f' Finished running the mapped executor in {time_taken} seconds')
    assert time_taken< 5+1,f"The processes should take less than {seconds+1}seconds."





