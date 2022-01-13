from concurrent.futures import ThreadPoolExecutor, as_completed

def thread_func():
    ret = []
    while not thread_task.empty():
        try:
            task = thread_task.get_nowait().strip()
        except:
            exit()
        ret.append(do_something(task))
    return ret


thread_task = queue.Queue()
with ThreadPoolExecutor(threadnum) as executor:
        future_list = [executor.submit(thread_func) for i in range(threadnum)]
    # threadpool return
    all_ret = []
    for future in as_completed(future_list):
        if future.result():
            all_ret.extend(future.result())