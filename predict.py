import numpy as np

Layers = (784, 25, 25, 10)


def sigmoid(z):
        return 1 / (1 + pow(np.e, -z))


def unflatten(theta):
    param = []
    start = 0
    end = 0
    for i in range(0, len(Layers) - 1):
        end += Layers[i + 1] * (Layers[i] + 1)
        param.append(theta[start:end].reshape(Layers[i + 1], Layers[i] + 1))
        start = end
    return param


# X is a 28 x 28 numpy array, theta is the flattened parameters, factors is the normalization constants
def front_prop(x, theta, fact):
    x = x.flatten()
    for i in range(0, len(x)):
        if fact[i * 2 + 1] != 0:
            x[i] = (x[i] - fact[i * 2]) / fact[i * 2 + 1]
        else:
            x[i] = 0
    x = np.hstack((1, x))
    thetas = unflatten(theta)
    a = [x]
    z = []
    for i in range(0, len(thetas)):
        z.append(np.matmul(thetas[i], a[i]))
        a_val = sigmoid(z[i])
        if i != len(thetas) - 1:
            a_val = np.hstack((1, a_val))
        a.append(a_val)
    return a[-1]