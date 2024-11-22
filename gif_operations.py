import glob
import os

from PIL import Image

from file_operations import create_folder


def generate_gif(fp_in):
    create_folder(fp_in)
    # Create the frames
    frames = []
    # Get list of all files only in the given directory
    list_of_files = filter(os.path.isfile,
                           glob.glob(fp_in + '/*.png'))
    # Sort list of files based on last modification time in ascending order
    list_of_files = sorted(list_of_files,
                           key=os.path.getmtime)
    for img in list_of_files:
        new_frame = Image.open(img)
        frames.append(new_frame)
    # Save into a GIF file that loops forever
    frames[0].save('png_to_gif.gif', format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=300, loop=0)
