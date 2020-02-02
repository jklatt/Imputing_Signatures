import matplotlib.pyplot as plt
import numpy as np
import torch


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def augment_labels(labels, n_samples):
    """Expand labels for multiple MC samples in the GP Adapter.

    Args:
         Takes tensor of size [n]

    Returns:
        expanded tensor of size [n_mc_samples, n]

    """
    return labels.expand(labels.shape[0], n_samples).transpose(1, 0)


def plot_losses(losses, losses_std=None, save_file=None):
    """Plot a dictionary with per epoch losses.

    Args:
        losses: Mean of loss per epoch
        losses_std: stddev of loss per epoch

    """
    for key, values in losses.items():
        if losses_std is not None:
            plt.errorbar(range(len(values)), values, yerr=losses_std[key], label=key)
        else:
            plt.plot(range(len(values)), values, label=key)
    plt.xlabel('# epochs')
    plt.ylabel('loss')
    plt.legend()
    if save_file:
        plt.savefig(save_file, dpi=200)
        plt.close()


def convert_to_base_type(value):
    """Convert a value into a python base datatype.

    Args:
        value: numpy or torch value

    Returns:
        Python base type
    """
    if isinstance(value, (torch.Tensor, np.generic)):
        return value.item()
    else:
        return value