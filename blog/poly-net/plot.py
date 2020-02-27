#!/usr/bin/env python3

import sys
import argparse
import numpy as np
from matplotlib import pyplot as plt
import pickle

def load_pickle(fname):
    with open(fname, 'rb') as f:
        return pickle.load(f)


def show_or_save(fname, show=True):
    if show:
        plt.show()
    else:
        plt.savefig(fname)
    plt.clf()


def f(x):
    return 6 + (2 * x) - (x ** 2) + 0.5 * (x ** 3)


def plot_solution(args):
    pred_history = load_pickle('poly.pred_history.dat')
    epochs_preds = [(x[0] * args.interval, x[1]) for x in
                    enumerate(pred_history[0::args.interval])]
    epochs_preds += [(len(pred_history) - 1, pred_history[-1])]

    step = (args.end - args.start) / args.num_points
    x = np.arange(args.start, args.end, step)
    y = f(x)
    if args.individual:
        for epoch, pred in epochs_preds:
            plt.plot(x, y, label='analytic')
            plt.plot(x, pred, label=f'epoch {epoch}')
            plt.legend()
            show_or_save(f'plot_{epoch:04}.png', show=args.show)
    else:
        plt.plot(x, y, label='analytic', linewidth=3.0)
        for epoch, pred in epochs_preds:
            plt.plot(x, pred, label=f'epoch {epoch}', linestyle=':',
                     linewidth=3.0)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        show_or_save('solution_plot.png', show=args.show)


def plot_loss(args):
    loss_history = load_pickle('poly.loss_history.dat')
    plt.plot(np.arange(len(loss_history)), loss_history)
    plt.xlabel('epoch')
    plt.ylabel('$\mathcal{L}$')
    show_or_save('loss_plot.png', show=args.show)


def parse_arguments(args):
    parser = argparse.ArgumentParser(description='plot polynomial')
    parser.add_argument('start',
                        type=float,
                        help='first value in domain')
    parser.add_argument('end',
                        type=float,
                        help='last value in domain')
    parser.add_argument('--num_points',
                        default=100,
                        help='num points on domain')
    parser.add_argument('--interval',
                        default=500,
                        type=int,
                        help='plot every interval epoch')
    parser.add_argument('--individual',
                        action='store_true',
                        help='draw each epoch on its own plot')
    parser.add_argument('--show',
                        action='store_true',
                        help='show instead of save plots')
    retval = parser.parse_args(args)
    if retval.end < retval.start:
        print('start must be less than end', file=sys.stderr)
        parser.print_help()
        sys.exit(-1)
    return retval


def main():
    args = parse_arguments(sys.argv[1:])
    plot_solution(args)
    plot_loss(args)


if __name__ == '__main__':
    main()
