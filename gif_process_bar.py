import argparse
import math
from PIL import Image, ImageSequence, ImageFile
# for very big images
ImageFile.LOAD_TRUNCATED_IMAGES = True

def fill_color(frame, left, right, bottom, top, color):
    for x in range(left, right):
        for y in range(bottom, top):
            frame.putpixel((x,y), color)
    return frame

def hex_to_rgb(hex_str:str)->tuple[int,int,int]:
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2 ,4))

def draw_bar(frame, width, height, bar_height, process, bg_color, bar_color):
    bar_width = math.ceil(width * process)
    frame = fill_color(frame, 0, bar_width, height-bar_height, height, bar_color);
    return fill_color(frame, bar_width, width, height-bar_height, height, bg_color);

def add_process_to_gif(from_path:str, to_path:str, bg_color:str ,bar_color:str):
    bg_color = hex_to_rgb(bg_color)
    bar_color = hex_to_rgb(bar_color) 
    frames = []
    duration = []
    with Image.open(from_path) as original:
        width, height = original.size
        frame_num = original.n_frames
        for index in range(frame_num):
            original.seek(index)
            new_frame = Image.new('RGBA', original.size)
            new_frame.paste(original)    
            draw_bar(new_frame, width, height, 5, index/frame_num, bg_color, bar_color)
            frames.append(new_frame)
            duration.append(original.info['duration'])
        frames[0].save(to_path, format='GIF', append_images=frames[1:], save_all=True, duration=duration, loop=0)  
       
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add a progress bar to a GIF image.')
    parser.add_argument('from_path', type=str,
                        help='the path of the original GIF image')
    parser.add_argument('to_path', type=str,
                        help='the path of the new GIF image')
    parser.add_argument('bg_color', type=str,
                        help='the background color of the progress bar in hex format')
    parser.add_argument('bar_color', type=str,
                        help='the color of the progress bar in hex format')
    args = parser.parse_args()

    add_process_to_gif(args.from_path,args.to_path,args.bg_color ,args.bar_color )
        
