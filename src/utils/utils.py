import os
import shutil

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