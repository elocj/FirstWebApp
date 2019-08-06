import numpy as np
from convoNN.conv import Conv3x3
from convoNN.maxpool import MaxPool2
from convoNN.softmax import Softmax

conv = Conv3x3(8)
pool = MaxPool2()
softmax = Softmax(47 * 47 * 8, 2)

class Action:
  def __init__(self, y_train):
    data = np.load('/Users/anthonyjoo/Google Drive/Python/FirstWebApp/convoNN/datatemp.npy')
    self.x_train = data[:450]
    self.y_train = np.zeros(450).astype(int)
    self.x_test = data[450:]
    self.y_test = np.zeros(147).astype(int)
    # self.run()

  def forward(self, image, label):
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
    out = softmax.forward(out)

    # Calculate cross-entropy loss and accuracy. np.log() is the natural log.
    loss = -np.log(out[label])
    acc = 1 if np.argmax(out) == label else 0

    return out, loss, acc

  def train(self, im, label, lr=.005):
    '''
    Completes a full training step on the given image and label.
    Returns the cross-entropy loss and accuracy.
    - image is a 2d numpy array
    - label is a digit
    - lr is the learning rate
    '''
    # Forward
    out, loss, acc = self.forward(im, label)

    # Calculate initial gradient
    gradient = np.zeros(2)
    gradient[label] = -1 / out[label]

    # Backprop
    gradient = softmax.backprop(gradient, lr)
    gradient = pool.backprop(gradient)
    gradient = conv.backprop(gradient, lr)

    return loss, acc

  def run(self):
    print('MNIST CNN initialized!')

    # Train the CNN for 3 epochs
    for epoch in range(1):
      print('--- Epoch %d ---' % (epoch + 1))

      # Shuffle the training data
      permutation = np.random.permutation(len(self.x_train))
      self.x_train = self.x_train[permutation]
      self.y_train = self.y_train[permutation]

      # Train!
      loss = 0
      num_correct = 0
      for i, (im, label) in enumerate(zip(self.x_train, self.y_train)):
        if i > 0 and i % 100 == 99:
          print('[Step %d] Past 100 steps: Average Loss %.3f | Accuracy: %d%%' % (i + 1, loss / 100, num_correct))
          # print(softmax.weights)
          loss = 0
          num_correct = 0

        l, acc = self.train(im, label)
        loss += l
        num_correct += acc

    # Test the CNN
    # find way to input the weights
    # print('\n--- Testing the CNN ---')
    # loss = 0
    # num_correct = 0
    # for im, label in zip(self.x_test, self.y_test):
    #   _, l, acc = self.forward(im, label)
    #   loss += l
    #   num_correct += acc
    #
    # num_tests = len(self.x_test)
    # print('Test Loss:', loss / num_tests)
    # print('Test Accuracy:', num_correct / num_tests)
    return softmax.weights