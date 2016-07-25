import utils.utilities as utils

#################
#  Model Flags  #
#################

def model_flags(model_name, flags):

    """
    :param flags:
    :return: self
    """

    flags.DEFINE_string('model_name', model_name, 'Model name.')
    flags.DEFINE_string('main_dir', model_name+'/', 'Directory to store data relative to the algorithm.')

    flags.DEFINE_integer('num_epochs', 20, 'Number of training epochs.')
    flags.DEFINE_integer('batch_size', 500, 'Size of each training mini-batch.')
    flags.DEFINE_float('xavier_init', 1, 'Value for the constant in xavier weights initialization.')
    flags.DEFINE_string('opt', 'adam', 'Optmization algorithm. {}'.format(utils.valid_optimization_functions))
    flags.DEFINE_float('learning_rate', 0.01, 'Initial learning rate.')
    flags.DEFINE_float('momentum', 0.5, 'Momentum parameter.')

    flags.DEFINE_integer('verbose', 1, 'Level of verbosity. 0 - silent, 1 - print accuracy.')
    flags.DEFINE_integer('seed', -1, 'Seed for the random generators (>= 0). Useful for testing hyperparameters.')

    flags.DEFINE_string('train_dataset', '', 'Path to train set file (.npy or .csv).')
    flags.DEFINE_string('test_dataset', '', 'Path to test set file (.npy or .csv).')
    flags.DEFINE_string('valid_dataset', '', 'Path to validation set file (.npy or .csv).')
    flags.DEFINE_boolean('restore_model', False, 'If true, restore previous model corresponding to model name.')



############################
#  Supervised Model Flags  #
############################

def set_supervised_model_global_flags(model_name, flags):

    """
    :param model_name:
    :param flags:
    :return: self
    """

    model_flags(model_name, flags)

    flags.DEFINE_string('train_labels', '', 'Path to train labels file (.npy or .csv).')
    flags.DEFINE_string('test_labels', '', 'Path to test labels file (.npy or .csv).')
    flags.DEFINE_string('valid_labels', '', 'Path to validation labels file (.npy or .csv).')

    flags.DEFINE_string('save_predictions', '', 'Path to a .npy file to save predictions for the test set.')


def set_supervised_model_flags(model_name, flags):

    """
    :param model_name:
    :param flags:
    :return: self
    """

    set_supervised_model_global_flags(model_name, flags)

    flags.DEFINE_string('enc_act_func', 'relu', 'Activation function for the hidden layers. {}'.format(utils.valid_act_functions))
    flags.DEFINE_string('dec_act_func', 'none', 'Activation function for the output layer. {}'.format(utils.valid_act_functions))
    flags.DEFINE_string('cost_func', 'rmse', 'Cost function. {}'.format(utils.valid_supervised_cost_functions))
    flags.DEFINE_float('dropout', 1.0, 'Hidden layers dropout.')
    flags.DEFINE_string('task', 'regression', 'Which type of task to perform. ["regression", "classification"]')



##############################
#  Unsupervised Model Flags  #
##############################

def set_unsupervised_model_global_flags(model_name, flags):

    """
    :param model_name:
    :param flags:
    :return: self
    """

    model_flags(model_name, flags)

    flags.DEFINE_boolean('save_encode_train', '', 'Path to a .npy file to save the encoded training data.')
    flags.DEFINE_boolean('save_encode_test', '', 'Path to a .npy file to save the encoded testing data.')
    flags.DEFINE_boolean('save_encode_valid', '', 'Path to a .npy file to save the encoded validation data.')


def set_unsupervised_model_flags(model_name, flags):

    """
    :param model_name:
    :param flags:
    :return: self
    """

    set_unsupervised_model_global_flags(model_name, flags)

    flags.DEFINE_string('enc_act_func', 'relu', 'Activation function for the encoder layer. {}'.format(utils.valid_act_functions))
    flags.DEFINE_string('dec_act_func', 'none', 'Activation function for the decode layer. {}'.format(utils.valid_act_functions))
    flags.DEFINE_string('cost_func', 'rmse', 'Cost function. {}'.format(utils.valid_unsupervised_cost_functions))