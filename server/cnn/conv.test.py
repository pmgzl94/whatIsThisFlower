import unittest
import numpy
import os

from tensor.Tensor import TensorFileManager

import conv
import pool

import dataloader

import adam

class TestConvNetwork(unittest.TestCase):
    
    def test_sliding_window3d_1(self):
        input = numpy.ndarray((3, 4, 3))
        conv1 = conv.ConvLayer(nb_filters=64)

        output = conv1.slidingWindow(input)
        self.assertEqual(output.shape, (64, 3, 2))
    
    # def test_sliding_window2d_1(self):
    #     input = numpy.ndarray((3, 4, 3))
    #     conv1 = conv.ConvLayer(nb_filters=64)

    #     output = conv1.slidingWindow(input)
    #     self.assertEqual(output.shape, (64, 3, 2))

    def test_sliding_window_2(self):
        pathdir = "./tensorfiles"
        filename = "conv_sliding_window2"
        fullypath = pathdir + "/" + filename
        if not os.path.exists(os.path.join(pathdir, filename + ".bs1.npy")):
            tm = TensorFileManager("./tensorfiles")

            containerfilter = numpy.ndarray((0, 3, 2, 2))

            f3 = numpy.array([[[3, 3], [3, 3]], [[3, 3], [3, 3]], [[3, 3], [3, 3]]])
            containerfilter = numpy.insert(containerfilter, 0, f3, 0)
            f2 = numpy.array([[[2, 2], [2, 2]], [[2, 2], [2, 2]], [[2, 2], [2, 2]]])
            containerfilter = numpy.insert(containerfilter, 0, f2, 0)
            f1 = numpy.array([[[1, 1], [1, 1]], [[1, 1], [1, 1]], [[1, 1], [1, 1]]])
            containerfilter = numpy.insert(containerfilter, 0, f1, 0)

            biases = numpy.zeros((3,))
            
            tm.save("conv_sliding_window2.bs1", biases)
            tm.save("conv_sliding_window2.ws1", containerfilter)
        
        conv1 = conv.ConvLayer(load_path="conv_sliding_window2")
        input = numpy.ones((3, 4, 3))
        output = conv1.slidingWindow(input)
        self.assertEqual(output.shape, (3, 3, 2))
        
        expected_o1 = numpy.ones((3,2)) * 12
        self.assertEqual((output[0] == expected_o1).all(), True)
        expected_o2 = numpy.ones((3,2)) * 24
        self.assertEqual((output[1] == expected_o2).all(), True)
        expected_o3 = numpy.ones((3,2)) * 36
        self.assertEqual((output[2] == expected_o3).all(), True)

    # #test for compute test for delta test
    # def test_get_nabla_w(self):
    #     # example from here: https://datascience.stackexchange.com/questions/27506/back-propagation-in-cnn
        
    #     # conv layer initialisation
    #     pathdir = "./tensorfiles"
    #     filename1 = "convtest"

    #     input = numpy.array([(0.51, 0.9, 0.88, 0.84, 0.05), 
    #           (0.4, 0.62, 0.22, 0.59, 0.1), 
    #           (0.11, 0.2, 0.74, 0.33, 0.14), 
    #           (0.47, 0.01, 0.85, 0.7, 0.09),
    #           (0.76, 0.19, 0.72, 0.17, 0.57)])

    #     if not os.path.exists(os.path.join(pathdir, filename1 + ".bs1.npy")):
    #         filter = numpy.array([[-0.13,0.15], [-0.51, 0.62]])
    #         biases = numpy.zeros((1,))
    #         tm = TensorFileManager("./tensorfiles")
    #         tm.save("convtest.bs1", biases)
    #         tm.save("convtest.ws1", filter)
        
    #     l1 = conv.ConvLayer(load_path=filename1, pool=pool.PoolLayer(), activation_function="sigmoid")
        
    #     res1 = l1.compute(input)
        
    #     #create layer 2
    #     # filename2 = "networktest"
    #     # if not os.path.exists(os.path.join(pathdir, filename2 + ".bs1.npy")):
    #     #     # ws = numpy.array([[0.61,0.82,0.96,-1], [0.02, -0.5, 0.23, 0.17]])
    #     #     # biases = numpy.zeros((2,))
    #     #     tm = TensorFileManager("./tensorfiles")
    #     #     tm.save("networktest.bs1", biases)
    #     #     tm.save("networktest.ws1", ws)
    #     ws = numpy.array([[0.61,0.82,0.96,-1], [0.02, -0.5, 0.23, 0.17]])
        
    #     prev_delta = numpy.array([0.25, -0.15]) #delta from the link

    #     delta = numpy.dot(prev_delta, ws)

    #     expected_result = numpy.array([[ 0.044606, 0.094061], [ 0.011262, 0.068288]])

    #     l1.learn(delta)

    #     result = l1.getNablaW()

    #     # self.assertEqual((result == expected_result).all(), True)
    #     self.assertEqual(numpy.isclose(result, expected_result, atol=1e-2).all(), True)
    
    # def test_get_next_delta1(self):
    #     # input = (5, 5)
    #     # filter = (2, 2)

    #     pathdir = "./tensorfiles"
    #     filename1 = "conv_next_delta_test"

    #     input = numpy.array([[0.1, 2, 0.11, 0.3, 1], [0, 0.4, 0.4, 0.36, 1], 
    #                         [0, 0.12, 0.27, 0.34, -3], [0.62, 0.12, 0.11, 10, 1], 
    #                         [0, 56, 11, 23, 44]])

    #     if not os.path.exists(os.path.join(pathdir, filename1 + ".bs1.npy")):
    #         filter = numpy.array([[-0.13,0.15], [-0.51, 0.62]])
    #         biases = numpy.zeros((1,))
    #         tm = TensorFileManager("./tensorfiles")

    #         tm.save(filename1 + ".bs1", biases)
    #         tm.save(filename1 + ".ws1", filter)
        
    #     l1 = conv.ConvLayer(load_path=filename1, pool=pool.PoolLayer(), activation_function="sigmoid")
        
    #     res1 = l1.compute(input)
        
    #     ws = numpy.array([[0.61,0.82,0.96,-1], [0.02, -0.5, 0.23, 0.17]])
        
    #     prev_delta = numpy.array([0.25, -0.15]) #delta from the link

    #     delta = numpy.dot(prev_delta, ws)

    #     l1.learn(delta)

    #     res = l1.getLastDelta()

    #     self.assertEqual(numpy.isclose(res[0][0], -0.004527013257), True)
    
    def test_get_next_delta2(self):
        # with depth and filter
        # input  = (3, 5, 5)
        # filter = (4, 3, 2, 2)

        pathdir = "./tensorfiles"
        filename1 = "conv_next_delta_test1"

        input = numpy.array([[[0.1, 2, 0.11, 0.3, 1], [0, 0.4, 0.4, 0.36, 1], 
                            [0, 0.12, 0.27, 0.34, -3], [0.62, 0.12, 0.11, 10, 1], 
                            [0, 0.56, 0.11, 0.44, 0.23]], [[0.1, 2, 0.11, 0.3, 1], [0, 0.4, 0.4, 0.36, 1], 
                            [0, 0.12, 0.27, 0.34, -3], [0.62, 0.12, 0.11, 10, 1], 
                            [0, 0.56, 0.11, 0.23, 0.44]], [[0.1, 2, 0.11, 0.3, 1], [0, 0.4, 0.4, 0.36, 1], 
                            [0, 0.12, 0.27, 0.34, -3], [0.62, 0.12, 0.11, 10, 1], 
                            [0, 0.56, 0.11, 0.23, 0.44]]])
        # print(f"input shape = {input.shape}")

        if not os.path.exists(os.path.join(pathdir, filename1 + ".bs1.npy")):
            f = numpy.array([[[-0.13,0.15], [-0.51, 0.62]], 
                    [[-0.13,0.15], [-0.51, 0.62]], [[-0.13,0.15], [-0.51, 0.62]]])
            
            containerfilter = numpy.ndarray((0, 3, 2, 2))

            containerfilter = numpy.insert(containerfilter, 0, f, axis=0)
            containerfilter = numpy.insert(containerfilter, 0, f, axis=0)
            containerfilter = numpy.insert(containerfilter, 0, f, axis=0)
            containerfilter = numpy.insert(containerfilter, 0, f, axis=0)

            #print(f"container filter shape = {containerfilter.shape}")

            biases = numpy.zeros((4,))

            tm = TensorFileManager("./tensorfiles")
            # print(f"shape = {f.shape}")

            tm.save(filename1 + ".bs1", biases)
            tm.save(filename1 + ".ws1", containerfilter)

        l1 = conv.ConvLayer(load_path=filename1, filtershape=(4, 3, 2, 2), pool=pool.PoolLayer(), activation_function="sigmoid")
    
        res1 = l1.compute(input)
        
        # print(f"result conv shape {res1.shape}")
        ws = numpy.array([[0.61,0.82,0.96,-1, 0.9, 0.71, 0.3, 0.276, 0.11, 0.12, 0.17, 0.5, 0.1, 0.2, 0.11, 0.6], 
                        [0.02, -0.5, 0.23, 0.17, 0.9, 0.1, 0.4, 0.9, 0.2, 0.12, 0.11, 0.3, 0.1, 0.2, 0.7, 0.8]])

        prev_delta = numpy.array([0.25, -0.15]) #delta from the link

        delta = numpy.dot(prev_delta, ws)

        # print(f"delta = {delta}")

        l1.learn(delta)

        dx = l1.getLastDelta()

        self.assertEqual(dx.shape, (3, 5, 5))

        # print(dx)

        self.assertEqual(numpy.isclose(dx[0][2][2], 2.837872562200001e-10), True)

    def test_bias_gradient1(self):
        train, test_data = dataloader.load_some_flowers(5, 0, crop_size=(0, 0, 150, 150))
        
        x = list(train)[0][0]

        c1 = conv.ConvLayer(filtershape=(32, 3, 3, 3), stride_length=1, pool=pool.PoolLayer(pool_size=(2, 2), stride_length=2), ishape=(3, 150, 150))
        
        out = c1.compute(x, learn=True)

        self.assertEqual(out.shape, (32, 74, 74))

        false_delta = numpy.ones((32, 74, 74))

        c1.learn(false_delta)
        
        nabla_b = c1.getNablaB()

        self.assertTrue(nabla_b.shape, (32,))
    
    def simple_adam_optimizer_test(self):
        train, test_data = dataloader.load_some_flowers(5, 0, crop_size=(0, 0, 150, 150))

        x = list(train)[0][0]
        
        c1 = conv.ConvLayer(optimizer=adam.AdamConv(), filtershape=(32, 3, 3, 3), stride_length=1, pool=pool.PoolLayer(pool_size=(2, 2), stride_length=2), ishape=(3, 150, 150))
        
        initFilters, initBiases = c1.getFiltersAndBiases()

        out = c1.compute(x, learn=True)

        false_delta = numpy.random.randn(*(32, 74, 74))

        c1.learn(false_delta)

        c1.modify_weights(learning_rate=0.1, batch_size=1)

        finalFilters, finalBiases = c1.getFiltersAndBiases()

        # print(f"init f {initFilters}")
        # print(f"final f {finalFilters}")

        self.assertFalse((initFilters == finalFilters).all())
        self.assertFalse((initBiases == finalBiases).all())







if __name__ == '__main__':
    unittest.main()