from PIL import Image

from resizeimage import resizeimage


with open('board.jpg', 'r+b') as f:
    with Image.open(f) as image:
        cover = resizeimage.resize_cover(image, [760, 760])
        cover.save('test-image-cover.jpeg', image.format)