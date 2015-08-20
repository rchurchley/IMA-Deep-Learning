from utils import *
import theano
import lasagne
from lasagne.layers import get_output, get_all_params


input_directory = 'data/solid+rect'
num_epochs = 10


def build_network(input_var=None):
    network = lasagne.layers.InputLayer(
        shape=(None, 1, 64, 64),
        input_var=input_var)

    network = lasagne.layers.Conv2DLayer(
        network, num_filters=1, filter_size=(1, 1),
        nonlinearity=None)

    network = lasagne.layers.DenseLayer(
        network,
        num_units=2,
        nonlinearity=lasagne.nonlinearities.softmax)

    return network


def build_model(input_var=None, target_var=None, network=None):
    def loss(test=False):
        return lasagne.objectives.categorical_crossentropy(
            get_output(network, deterministic=test), target_var).mean()

    optimizer = lasagne.updates.nesterov_momentum(
        loss(),
        get_all_params(network, trainable=True),
        learning_rate=0.01,
        momentum=0.01)

    return {
        'input_var': input_var,
        'target_var': target_var,
        'network': network,
        'loss': loss,
        'updates': optimizer
    }


def main(input_directory, num_epochs=5):
    print("Loading data...")
    data = load_datasets(input_directory)

    print("Building model...")
    input_var = theano.tensor.tensor4('inputs')
    target_var = theano.tensor.ivector('targets')
    network = build_network(input_var)
    model = build_model(input_var, target_var, network)

    print("Starting training...")
    train_network(data, model, num_epochs)

    print("\nLearned parameters:")
    for p in lasagne.layers.get_all_param_values(network):
        print p


if __name__ == '__main__':
    main(input_directory, num_epochs)
