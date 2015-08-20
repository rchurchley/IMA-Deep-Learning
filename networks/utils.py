import numpy
import theano
import theano.tensor
from lasagne.layers import get_output
import time


def load_datasets(input_directory):
    """Return the training, validation, and testing data and labels."""
    result = {'train': {}, 'validate': {}, 'test': {}}
    for dataset in result:
        for part in ['data', 'labels']:
            result[dataset][part] = numpy.load(
                '{}/{}_{}.npy'.format(input_directory, dataset, part))
    return result


def iterate_minibatches(inputs, targets, batchsize, shuffle=False):
    assert len(inputs) == len(targets)
    if shuffle:
        indices = numpy.arange(len(inputs))
        numpy.random.shuffle(indices)
    for start_idx in range(0, len(inputs) - batchsize + 1, batchsize):
        if shuffle:
            excerpt = indices[start_idx:start_idx + batchsize]
        else:
            excerpt = slice(start_idx, start_idx + batchsize)
        yield inputs[excerpt], targets[excerpt]


def full_pass(input_dict, val_fn):
    total_err = 0
    total_acc = 0
    total_batches = 0
    for batch in iterate_minibatches(input_dict['data'],
                                     input_dict['labels'],
                                     1,
                                     shuffle=False):
        inputs, targets = batch
        err, acc = val_fn(inputs, targets)
        total_err += err
        total_acc += acc
        total_batches += 1
    return total_err, total_acc, total_batches


def train_network(inputs, model, num_epochs):
    network = model['network']

    test_acc = theano.tensor.mean(
        theano.tensor.eq(
            theano.tensor.argmax(
                get_output(
                    network,
                    deterministic=True),
                axis=1),
            model['target_var']),
        dtype=theano.config.floatX)

    # Compile functions
    train_fn = theano.function(
        [model['input_var'], model['target_var']],
        model['loss'](),
        updates=model['updates'])

    val_fn = theano.function(
        [model['input_var'], model['target_var']],
        [model['loss'](test=True), test_acc])

    print("\n{:>5} {:>17} {:>17} {:>10} {:>10}".format(
        'Epoch', 'Training loss', 'Validation loss', 'Accuracy', 'Time (s)'))
    for epoch in range(num_epochs):
        train_err = 0
        train_batches = 0
        start_time = time.time()
        for batch in iterate_minibatches(inputs['train']['data'],
                                         inputs['train']['labels'],
                                         1,
                                         shuffle=True):
            batch_inputs, batch_targets = batch
            train_err += train_fn(batch_inputs, batch_targets)
            train_batches += 1

        val_err, val_acc, val_batches = full_pass(inputs['validate'], val_fn)
        print("{:>5} {:>17.5f} {:>17.5f} {:>10.3%} {:>10.3f}".format(
            epoch + 1,
            train_err / train_batches,
            val_err / val_batches,
            val_acc / val_batches,
            time.time() - start_time))

    print("\nFinal results:")
    final_err, final_acc, final_batches = full_pass(inputs['test'], val_fn)
    print("Loss: {}".format(final_err / final_batches))
    print("Accuracy: {:.3%}".format(final_acc / final_batches))

