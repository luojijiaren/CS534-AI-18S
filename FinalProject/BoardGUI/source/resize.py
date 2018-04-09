from PIL import Image
import glob, os

im1 = Image.open("background.jpg")
im5 = im1.resize((760, 760), Image.ANTIALIAS)    # best down-sizing filter
im5.save("new_back.jpg")