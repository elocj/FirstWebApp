import numpy as np
from conv import Conv3x3
from maxpool import MaxPool2
from softmax import Softmax

data = np.load('data.npy')
x_train = data[:450]
y_train = []
x_test = data[450:]
y_test = np.ones(147).astype(int)

conv = Conv3x3(8)
pool = MaxPool2()
softmax = Softmax(849 * 849 * 8, 2)

def forward(image, label):
    out = conv.forward((image / 255) - 0.5)
    out = pool.forward(out)
    out = softmax.forward(out)

    loss = -np.log(out[label])
    acc = 1 if np.argmax(out) == label else 0
    return out, loss, acc

print('MNIST CNN initialized!')

loss = 0
num_correct = 0
for i, (im, label) in enumerate(zip(x_test, y_test)):
    _, l, acc = forward(im, label)
    loss += l
    num_correct += acc
    if i % 100 == 99:
      print('[Step %d] Past 100 steps: Average Loss %.3f | Accuracy: %d%%' % (i + 1, loss / 100, num_correct))
      loss = 0
      num_correct = 0