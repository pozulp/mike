#!/usr/bin/env python3

__version__ = '0.0.1'

import os
import sys
import argparse
import numpy as np
import torch
import pickle
try:
    from torch.utils.tensorboard import SummaryWriter
    have_tensorboard = True
except Exception as e:
    have_tensorboard = False
    import_exception = e


NUM_TRAINING_POINTS = 100
NUM_HIDIDEN_LAYER_NODES = 5
EPSILON = 1e-3
LOSS_PRINT_INTERVAL = 500


def print_version():
    py = sys.version_info
    names_versions = [('python', f'{py.major}.{py.minor}.{py.micro}')]
    for package in [np, torch]:
        names_versions += [(package.__name__, package.__version__)]

    header = f'{os.path.basename(__file__)} {__version__}'
    print(header)
    print('-' * len(header))
    for name, version in names_versions:
        print(f'{name} {version}')


def write_pickle_to_file(data, ext):
    fname = f'poly.{ext}.dat'
    with open(fname, 'wb') as f:
        pickle.dump(data, f)


def f(x):
    return 6 + (2 * x) - (x ** 2) + 0.5 * (x ** 3)


def parse_arguments(args):
    parser = argparse.ArgumentParser(description='plot polynomial')
    parser.add_argument('start',
                        type=float,
                        help='first value in domain')
    parser.add_argument('end',
                        type=float,
                        help='last value in domain')
    parser.add_argument('--num_training_points',
                        default=NUM_TRAINING_POINTS,
                        help='num points on domain for training')
    parser.add_argument('--num_hidden_layer_nodes',
                        default=NUM_HIDIDEN_LAYER_NODES,
                        help='num nodes in the hidden layer')
    parser.add_argument('--epsilon',
                        type=float,
                        default=EPSILON,
                        help='convergence criterion')
    parser.add_argument('--loss_print_interval',
                        default=LOSS_PRINT_INTERVAL,
                        help='print loss every loss_print_interval epochs')
    if have_tensorboard:
        parser.add_argument('--tensorboard',
                            action='store_true',
                            help='generate summary data for tensorboard')
    retval = parser.parse_args(args)
    if retval.end < retval.start:
        print('start must be less than end', file=sys.stderr)
        parser.print_help()
        sys.exit(-1)
    return retval


def calculate_loss(y_pred, x):
    loss = torch.norm(y_pred - f(x))
    return loss


def train(args, x, model, optimizer, num_iterations_estimate=2**20):
    loss_history = np.zeros(num_iterations_estimate)
    pred_history = np.zeros((num_iterations_estimate, len(x)))
    prev_loss = 1e6
    it = 0
    while True:
        y_pred = model(x)
        pred_history[it] = y_pred.detach().numpy().flatten()
        loss = calculate_loss(y_pred, x)
        loss_history[it] = loss
        if it % args.loss_print_interval == 0:
            print(f'Iter {it}:', loss.item())

        optimizer.zero_grad()

        loss.backward()

        optimizer.step()

        loss = loss.item()
        err = np.abs(loss - prev_loss)
        prev_loss = loss

        if err < args.epsilon:
            break
        it += 1
    return loss_history[:it], pred_history[:it]


def main():
    args = parse_arguments(sys.argv[1:])
    if have_tensorboard and args.tensorboard:
        writer = SummaryWriter()
    model = torch.nn.Sequential(
                torch.nn.Linear(1, args.num_hidden_layer_nodes),
                torch.nn.Tanh(),
                torch.nn.Linear(args.num_hidden_layer_nodes, 1))
    optimizer = torch.optim.Adam(model.parameters())
    x = torch.linspace(args.start, args.end, args.num_training_points,
                       requires_grad=True)
    x = x[:, None]
    if have_tensorboard and args.tensorboard:
        writer.add_graph(model, x)
    loss_history, pred_history = train(args, x, model, optimizer)
    write_pickle_to_file(args, 'args')
    write_pickle_to_file(loss_history, 'loss_history')
    write_pickle_to_file(pred_history, 'pred_history')
    write_pickle_to_file(model, 'model')


if __name__ == '__main__':
    main()
