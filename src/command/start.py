import os

def start(directory, max_audio_filesize, allowed_formats):

    print(directory)
    print(max_audio_filesize)
    # 1. Find all audio files in the directory below 25MB
    
    allowed_files = get_all_allowed_files(os.listdir(directory), 
                                          conditions=[
                                              lambda fn: os.path.getsize(directory + '/' + fn) < max_audio_filesize, 
                                              lambda fn: fn.split('.')[-1] in allowed_formats
                                          ])

    print(allowed_files)

    # create mikhail directory and its subdirectories


    # create all transcript files
    


def get_all_allowed_files(file_list, conditions):
    allowed_files = [file_name for file_name in file_list if all([condition(file_name) for condition in conditions])]

    return allowed_files
            
    