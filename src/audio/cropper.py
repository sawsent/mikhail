import ffmpeg

def crop_into(input_path: str, output_path: str, start: float, end: float, loglevel='quiet'):

    try:
        (
            ffmpeg
            .input(input_path, ss=start, t=end-start)
            .output(output_path, loglevel=loglevel)
            .run(overwrite_output=True)  
        )
    except ffmpeg.Error as e:
        print(f"Error occurred during conversion of file '{input_path}'") 

