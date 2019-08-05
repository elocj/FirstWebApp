import numpy as np
from conv import Conv3x3
from maxpool import MaxPool2
from softmax import Softmax

# print(trainY)
import random

# y_train = []
# for _ in range(450):
#     k = random.randint(0, 1) # decide on a k each time the loop runs
#     y_train.append(k)

# supposed to be one hot key
# y_train = np.array(y_train)
data = np.load('datatemp.npy')
# x_train = data[:450]
x_train = data[:450]
y_train = np.zeros(450).astype(int)
# y_train = []
# x_test = data[450:]
# y_test = np.ones(147).astype(int)
#591
x_test = data[450:]
y_test = np.zeros(147).astype(int)

x_test = data[5:]
y_test = np.ones(len(data) - 5).astype(int)

conv = Conv3x3(8)
pool = MaxPool2()
softmax = Softmax(47 * 47 * 8, 2)

def forward(image, label):
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

def train(im, label, lr=.005):
  '''
  Completes a full training step on the given image and label.
  Returns the cross-entropy loss and accuracy.
  - image is a 2d numpy array
  - label is a digit
  - lr is the learning rate
  '''
  # Forward
  out, loss, acc = forward(im, label)

  # Calculate initial gradient
  gradient = np.zeros(2)
  gradient[label] = -1 / out[label]

  # Backprop
  gradient = softmax.backprop(gradient, lr)
  gradient = pool.backprop(gradient)
  gradient = conv.backprop(gradient, lr)

  return loss, acc

print('MNIST CNN initialized!')

# Train the CNN for 3 epochs
for epoch in range(3):
  print('--- Epoch %d ---' % (epoch + 1))

  # Shuffle the training data
  permutation = np.random.permutation(len(x_train))
  x_train = x_train[permutation]
  y_train = y_train[permutation]

  # Train!
  loss = 0
  num_correct = 0
  for i, (im, label) in enumerate(zip(x_train, y_train)):
    if i > 0 and i % 100 == 99:
      print('[Step %d] Past 100 steps: Average Loss %.3f | Accuracy: %d%%' % (i + 1, loss / 100, num_correct))
      loss = 0
      num_correct = 0

    l, acc = train(im, label)
    loss += l
    num_correct += acc

# Test the CNN
print('\n--- Testing the CNN ---')
loss = 0
num_correct = 0
for im, label in zip(x_test, y_test):
  _, l, acc = forward(im, label)
  loss += l
  num_correct += acc

num_tests = len(x_test)
print('Test Loss:', loss / num_tests)
print('Test Accuracy:', num_correct / num_tests)