import os
from PIL import Image
import numpy as np

#root = 'images/'
# for subdir, dirs, files in os.walk(root):
#     for file in files:
#         imageObject = Image.open(os.path.join('images/', file))
#         cropped = imageObject.crop((400, 18, 2100, 1718))
#         cropped.save(os.path.join('image/', file))
# script for cropping pics

# rootdir = 'C:/Users/ajoo/Documents/CFD Version 2.0.3/CFD 2.0.3 Images'
# for subdir, dirs, files in os.walk(rootdir):
#     for file in files:
#         if os.path.splitext(file)[1].lower() in ('.jpg', '.jpeg'):
#             print(os.path.join(subdir, file))
#             hey = os.path.join(subdir, file)
#             imageObject = Image.open(hey)
#             ff = imageObject
#             ff.save(os.path.join('images/', file))
#             break
# Script that just takes the first jpeg image out of each file directory

# data = []
# roots = '/Users/anthonyjoo/Google Drive/Python/FirstWebApp/static/newimg'
# for subdir, dirs, files in os.walk(roots):
#     for file in files:
#         img = Image.open(os.path.join('/Users/anthonyjoo/Google Drive/Python/FirstWebApp/static/newimg', file)).convert('L')
#         WIDTH, HEIGHT = img.size
#         d = list(img.getdata())
#         d = [d[offset: offset + WIDTH] for offset in range(0, WIDTH * HEIGHT, WIDTH)]
#         data.append(d)
# data = np.array(data)
# np.save('datatemp', data)
# print(data)
# Script to turn images into data

# from PIL import Image

# roots = '/Users/anthonyjoo/Google Drive/Python/FirstWebApp/static/images'
# for subdir, dirs, files in os.walk(roots):
#     for file in files:
#         img = Image.open(os.path.join('/Users/anthonyjoo/Google Drive/Python/FirstWebApp/static/images', file)).convert('L')
#         new_img = img.resize((96, 96), Image.ANTIALIAS)
#         quality_val = 100  # you can vary it considering the tradeoff for quality vs performance
#         new_img.save(os.path.join('/Users/anthonyjoo/Google Drive/Python/FirstWebApp/static/downImages/', file), "JPEG", quality=quality_val)
# Resize an image