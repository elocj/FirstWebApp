import numpy as np
from convoNN.conv import Conv3x3
from convoNN.maxpool import MaxPool2
from convoNN.softmax import Softmax
import os
from PIL import Image

conv = Conv3x3(8)
pool = MaxPool2()
softmax = Softmax(47 * 47 * 8, 2)

# add a way to turn the images into grey scale matrix

class Test:
    def __init__(self, x_test, weights):
        self.x_test = x_test
        self.weights = weights

    def forward(self, image):
        '''
        Completes a forward pass of the CNN and calculates the accuracy and
        cross-entropy loss.
        - image is a 2d numpy array
        - label is a digit
        '''
        # We transform the image from [0, 255] to [-0.5, 0.5] to make it easier
        # to work with. This is standard practice.
        out = conv.forward((image / 255) - 0.5)
        out = pool.forward(out)
        softmax.weights = self.weights
        out = softmax.forward(out)

        return np.argmax(out)
        # acc = 1 if np.argmax(out) == label else 0
        #
        # return out, loss, acc

    def script(self):
        img = Image.open(os.path.join('/Users/anthonyjoo/Google Drive/Python/FirstWebApp/static/uploadImages', self.x_test)).convert('L')
        new_img = img.resize((96, 96), Image.ANTIALIAS)
        quality_val = 100  # you can vary it considering the tradeoff for quality vs performance
        new_img.save(os.path.join('/Users/anthonyjoo/Google Drive/Python/FirstWebApp/static/fixUploadImages/', self.x_test), "JPEG", quality=quality_val)
        # Resize an image

        data = []
        img = Image.open(os.path.join('/Users/anthonyjoo/Google Drive/Python/FirstWebApp/static/fixedUploadImages', self.x_test)).convert('L')
        WIDTH, HEIGHT = img.size
        d = list(img.getdata())
        d = [d[offset: offset + WIDTH] for offset in range(0, WIDTH * HEIGHT, WIDTH)]
        data.append(d)
        data = np.array(data)
        np.save('datatest', data)
        # Script to turn images into data

    def testIt(self):
        # Test the CNN
        #find way to input the weights
        self.script()
        self.x_test = np.load('/Users/anthonyjoo/Google Drive/Python/FirstWebApp/convoNN/datatest.npy')
        print('\n--- Testing the CNN ---')
        ans = self.forward(self.x_test)
        return ans