import numpy as np
import tensorflow as tf

# Constants
ONE = tf.constant(1.0)

valid_act_functions               = ['sigmoid', 'tanh', 'relu', 'none']
valid_supervised_cost_functions   = ['rmse', 'cross_entropy', 'softmax_cross_entropy']
valid_unsupervised_cost_functions = ['rmse', 'cross_entropy', 'softmax_cross_entropy', 'sparse']
valid_optimization_functions      = ['gradient_descent', 'ada_grad', 'momentum', 'adam', 'rms_prop']


# ################### #
#   Network helpers   #
# ################### #

def activate(act_f, input_layer):

    """
    :param act_f:
    :param input_layer:
    :return:
    """

    if act_f == 'sigmoid':
        return tf.nn.sigmoid(input_layer)

    elif act_f == 'tanh':
        return tf.nn.tanh(input_layer)

    elif act_f == 'relu':
        return tf.nn.relu(input_layer)

    if (act_f is None) or (act_f == 'none'):
        return input_layer

    else:
        raise Exception("Incorrect activation function")


def xavier_init(fan_in, fan_out, constant=1):

    """ Initialize values for the weights of a hidden layer i. It should be uniformly sampled from a symmetric
    interval that depends on the activation function.
    For 'tanh', constanta = 1.
    For 'sigmoid', constant = 4
    :param fan_in:
    :param fan_out:
    :param constant:
    :return:
    """
    low = -constant * np.sqrt(6.0 / (fan_in + fan_out))
    high = constant * np.sqrt(6.0 / (fan_in + fan_out))
    return tf.random_uniform((fan_in, fan_out), minval=low, maxval=high, dtype=tf.float32)


# ################ #
#   Data helpers   #
# ################ #

def gen_batches(data, batch_size):

    """ Divide input data into batches.
    :param data: input data
    :param batch_size: size of each batch
    :return: data divided into batches
    """
    data = np.array(data)

    for i in range(0, data.shape[0], batch_size):
        yield data[i:i+batch_size]


def normalize(data):

    """ Normalize the data to be in the [0, 1] range.
    :param data:
    :return: normalized data
    """

    out_data = data.copy()

    for i, sample in enumerate(out_data):
        out_data[i] /= sum(out_data[i])

    return out_data


# ############# #
#   Utilities   #
# ############# #

def expand_args(args_to_expand):

    """Expands all the lists in args_to_expand into the length of layers.
    This is used as a convenience so that the user does not need to specify the
    complete list of parameters for model initialization.
    IE: the user can just specify one parameter and this function will expand it
    :param args_to_expand:
    :return:
    """

    layers = args_to_expand['layers']

    for key, val in args_to_expand.items():
        if isinstance(val, list) and (len(val) != len(layers)):
            args_to_expand[key] = [val[0] for _ in layers]

    return args_to_expand


def flag_to_list(flag_val, dtype):

    """
    :param flag_val:
    :param dtype:
    :return:
    """

    if dtype == 'int':
        return [int(_) for _ in flag_val.split(',') if _]

    elif dtype == 'float':
        return [float(_) for _ in flag_val.split(',') if _]

    elif dtype == 'str':
        return [_ for _ in flag_val.split(',') if _]

    else:
        raise Exception("Incorrect data type")


