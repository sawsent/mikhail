import os
import shutil
import threading
import time

def build_path(*args) -> str:
    return os.path.join(*args)

def get_flat_directory(directory: str, return_list=[]) -> list[str]:
    all_in_dir = os.listdir(directory) 
    
    for file in [item for item in all_in_dir if not os.path.isdir(build_path(directory, item))]:
        return_list.append(build_path(directory, file))

    for dir in [item for item in all_in_dir if os.path.isdir(build_path(directory, item))]:
        get_flat_directory(build_path(directory, dir), return_list)

    return_list.append(directory)

    return return_list

def delete_all(to_delete) -> None:
    for item in to_delete:
        if os.path.isdir(item):
            os.rmdir(item)
        else:
            os.remove(item)

def delete_directory_with_tqdm(directory: str):
    from tqdm import tqdm
    to_delete = get_flat_directory(directory, [])
    delete_all(tqdm(to_delete))

def delete_directory_silent(directory: str):
    shutil.rmtree(directory) 

def animate_working(task, before='', after='', custom_animation=False):
    default_animation = [
        '█....', '.█...', '..█..', '...█.', '....█', '...█.', '..█..', '.█...'
    ]
    animation = custom_animation or default_animation
    def loading_task(stop_event):
        print(before, end=' ')
        idx = 0
        while not stop_event.is_set():
            print(animation[idx % len(animation)], end="", flush=True)
            time.sleep(0.1)
            print('\b' * len(animation[0]), end='', flush=True)
            idx += 1

        print('      ' + after)

    
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=loading_task, args=(stop_event,))
    spinner_thread.start()
    
    result = None

    try:
        result = task()
    finally:
        stop_event.set()
        spinner_thread.join()

    return result
