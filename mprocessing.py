from multiprocessing import Process
import time

def do_something():
    print('Sleeping 1 second...')
    time.sleep(1)
    print('Done sleeping...')


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


def do_something_with_args(seconds):
    print('Sleeping {seconds} second...')
    time.sleep(seconds)
    print('Sleeping {seconds} second...')



