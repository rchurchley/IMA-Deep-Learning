from utils import *
import theano
import lasagne
from lasagne.layers import get_output, get_all_params
from lasagne.updates import nesterov_momentum
from lasagne.objectives import categorical_crossentropy


def build_network(input_var=None):
    network = lasagne.layers.InputLayer(
        shape=(None, 1, 64, 64),
        input_var=input_var)

    network = lasagne.layers.Conv2DLayer(
        network, num_filters=3, filter_size=(9, 9),
        nonlinearity=lasagne.nonlinearities.rectify,
        W=lasagne.init.GlorotUniform())

    network = lasagne.layers.MaxPool2DLayer(network, pool_size=(1, 1))

    network = lasagne.layers.DenseLayer(
        network,
        num_units=2,
        nonlinearity=lasagne.nonlinearities.softmax)

    return network


def build_model(input_var=None, target_var=None, network=None):
    def loss(test=False):
        return categorical_crossentropy(
            get_output(network, deterministic=test), target_var).mean()

    optimizer = nesterov_momentum(
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


def main(num_epochs=5):
    print("Loading data...")
    data = load_datasets('data/solid+rect')

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
    main()
