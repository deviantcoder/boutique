from PIL import Image

img = Image.open('D:\\django\\boutique\\static\\images\\collection_images\\wp7953969-sunny-retro-ps4-wallpapers_revOH9T.jpg')

width, height = img.size

min_side = min(img.size)

left = (img.width - min_side) // 2
top = (img.height - min_side) // 2
right = (img.width + min_side) // 2
bottom = (img.height + min_side) // 2

img1 = img.crop((left, top, right, bottom))

img1.show()