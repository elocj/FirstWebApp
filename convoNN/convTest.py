import numpy as np
from convoNN.conv import Conv3x3
from convoNN.maxpool import MaxPool2
from convoNN.softmax import Softmax

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

    def testIt(self):
        # Test the CNN
        #find way to input the weights
        print('\n--- Testing the CNN ---')
        ans = self.forward(self.x_test)
        return ans