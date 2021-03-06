import numpy as np
import os

from tensor.Tensor import TensorFileManager
from layer import LayerInterface
import activation_functions
from adam import AdamFC

#mean squared error
def mse(output, expec_o):
    return np.sum((expec_o - output)**2) /len(output)

#cost functions
def basic_cost_derivative(y, a): #where y is the expected result
    return a - y

class FCLayer(LayerInterface):
    # def __init__(self, optimizer=None, arch=[784, 100, 10], load_path=None, is_classifier=True):
    def __init__(self, optimizer=None, load_path=None, arch=[784, 100, 10], activation_func="sigmoid", is_classifier=True):
        self.weights = []
        self.biases  = []

        self.optimizer = optimizer

        self.activation_func = activation_func

        self.afct, self.dafct = activation_functions.map_function[activation_func]
        self.is_classifier = is_classifier

        self.nb_layer = len(arch)
        self.nb_set_of_params = self.nb_layer - 1

        if load_path == None:
            for i in range(0, self.nb_set_of_params):
                # set_of_weights = np.random.randn(*(arch[i+1], arch[i])) * np.sqrt(1/(arch[i]))
                set_of_weights = np.random.randn(*(arch[i+1], arch[i])) * np.sqrt(2/(arch[i]))
                self.weights.append(set_of_weights)
                self.biases.append(np.zeros(arch[i+1]))
        else:
            self.load(load_path)
        self.inputshape = (self.weights[0].shape[1],)
        
        if self.optimizer:
            self.optimizer.setMomentumVars(self.weights, self.biases)

        #learning vars: used for backpropagation
        self.a = []
        self.z = []

        self.sum_of_nabla_w = []
        self.sum_of_nabla_b = []

        self.lastDelta = None

        self.resetLearningVars()

    def compute(self, input, learn=False):
        if len(input.shape) != 1:
            input = input.flatten()
        if input.shape != self.inputshape:
            raise Exception("wrong input shape")
        return self.forward(input, learn)

    def forward(self, input, learn=False):
        if len(input.shape) > 1:
            input = input.flatten()
        if input.shape[0] != self.weights[0].shape[1]:
            raise Exception(f"wrong input shape: received shape {input.shape}")

        self.a = []
        self.z = []
        
        x = input
        self.a = [x]
        for i in range(0, self.nb_set_of_params):
            z = np.dot(x, self.weights[i].T) + self.biases[i]
            x = self.afct(z)
            if learn == True:
                self.z.append(z)
                self.a.append(x)
        return x
    def getType(self):
        return "Dense"

    def learn(self, expected_res): #expected res or delta
        # expected_res = expected_res.flatten() #for the mnist dataset
        nabla_w = []
        nabla_b = []
        delta = None
        if self.is_classifier:
            delta = basic_cost_derivative(expected_res, self.a[-1]) * self.dafct(self.z[-1])
            nabla_w = [np.outer(delta, self.a[-2].T)]
            nabla_b = [delta]
        else:
            #expected res = delta . previous_weights
            delta = expected_res * self.dafct(self.z[-1]) #delta = delta+1. w.T(+1)
            nabla_w = [np.outer(delta, self.a[-2].T)]
            nabla_b = [delta]

        for index_set_param in range(self.nb_set_of_params - 2, -1, -1):
            delta = np.dot(delta, self.weights[index_set_param + 1]) * self.dafct(self.z[index_set_param])
            nabla_w.insert(0, np.outer(delta, self.a[index_set_param].T))
            nabla_b.insert(0, delta)
        
        self.lastDelta = delta
        self.sumUpNablas(nabla_w, nabla_b)
        
        return mse(self.a[-1], expected_res)

    def resetLearningVars(self):
        self.sum_of_nabla_w = []
        self.sum_of_nabla_b = []
        for i in range(0, self.nb_set_of_params):
            self.sum_of_nabla_w.append(np.zeros(self.weights[i].shape))
            self.sum_of_nabla_b.append(np.zeros(self.biases[i].shape))
        
        self.lastDelta = None
        self.a = []
        self.z = []
    
    
    def load(self, load_path):
        dir = "./tensorfiles"
        if not os.path.exists(dir + "/" + load_path + ".ws1.npy"):
            raise Exception("tensor file not exists")

        tfm = TensorFileManager(dir)
        self.weights, self.biases = tfm.loadNet(load_path, self.nb_set_of_params)

    def save(self, filename):
        tm = TensorFileManager("./tensorfiles")
        tm.saveNet(filename, self.weights, self.biases)
    
    #used for the sgd
    def sumUpNablas(self, nabla_w, nabla_b):
        for i in range(0, self.nb_set_of_params):
            self.sum_of_nabla_w[i] = self.sum_of_nabla_w[i] + nabla_w[i]
            self.sum_of_nabla_b[i] = self.sum_of_nabla_b[i] + nabla_b[i]

    def modify_weights(self, learning_rate, batch_size):
        if self.optimizer:
            mean_gw = []
            mean_gb = []
            for i in range(len(self.sum_of_nabla_w)):
                mean_gw.append(self.sum_of_nabla_w[i] / batch_size)
                mean_gb.append(self.sum_of_nabla_b[i] / batch_size)

            self.weights, self.biases = self.optimizer.update(self.weights, self.biases, mean_gw, mean_gb)

        else:
            for i in range(self.nb_set_of_params):
                self.weights[i] = self.weights[i] - (learning_rate/batch_size) * self.sum_of_nabla_w[i]
                self.biases[i] = self.biases[i] - (learning_rate/batch_size) * self.sum_of_nabla_b[i]
        
        self.resetLearningVars()

    def getWeightsAndBiases(self):
        return self.weights, self.biases
    
    def getLastDelta(self):
        return np.dot(self.lastDelta, self.weights[0])

    def getNablas(self):
        return self.sum_of_nabla_w, self.sum_of_nabla_b

# a = FcLayer(arch=[2, 3, 2])

# a.learn(np.array([1, 2]), np.array([1, 0]))