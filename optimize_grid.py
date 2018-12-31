import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import itertools
import numpy as np
from printer import set_up_logging, info
import os
from automated_batch_of_simulations import run_batch


def heatmap_of_results(quantifier, results_csv_path):
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.rcParams.update({'font.size': 16})
    sns.heatmap(
        ax=ax,
        data=pd.read_csv(results_csv_path)\
            .assign(percent_success=lambda df: -df.evaluation * 100)\
            .pivot('alpha', 'initial_temperature', 'percent_success'),
        linewidths=11, linecolor='white', cmap='inferno_r', cbar_kws={'format': '%.0f%%'})
    ax.set_title('Success Rate of SA Learner for Q-Det %s' % quantifier, fontdict={'size': 26})
    ax.set_ylabel('$\\alpha$', fontdict={'size': 28})
    ax.set_xlabel('Initial $T$', fontdict={'size': 24})
    ax.invert_yaxis()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(results_csv_path), 'opt_%s.png' % quantifier))


def f_inittemp_and_alpha(alpha, initial_temperature, quantifier_type, threshold, num_simulations, run_batch_kwargs):
    info('Starting grid search optimization iteration with:', alpha, initial_temperature, quantifier_type,
         threshold, num_simulations, run_batch_kwargs)
    total_success = run_batch(
        create_plots=False,
        base_seed=0,
        quantifier_type=quantifier_type,
        initial_temperature=initial_temperature,
        threshold=threshold,
        alpha=alpha,
        num_simulations=num_simulations,
        **run_batch_kwargs)
    return -total_success / float(num_simulations)


def optimize_inittemp_and_alpha(quantifier_type, alpha_domain, initial_temperature_domain,
                                threshold, num_simulations_in_each_batch, run_batch_kwargs):
    def opt_output_path(path):
        out_dir = os.path.join('opt_grid', 'opt_temperature_and_alpha', quantifier_type)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        return os.path.join(out_dir, path)

    info('Starting grid optimization')
    with open(opt_output_path('grid_eval.csv'), 'w') as f_results:
        f_results.write('evaluation,qunatifier,alpha,initial_temperature,threshold\n')
        for alpha, init_temp in itertools.product(alpha_domain, initial_temperature_domain):
            f_value = f_inittemp_and_alpha(
                alpha=alpha,
                initial_temperature=init_temp,
                quantifier_type=quantifier_type,
                threshold=threshold,
                num_simulations=num_simulations_in_each_batch,
                run_batch_kwargs=run_batch_kwargs)
            f_results.write(','.join(map(str, [f_value, quantifier_type, alpha, init_temp, threshold])) + '\n')
    info('Finished grid optimization')


if __name__ == '__main__':
    set_up_logging('out.log')
    # optimize_inittemp_and_alpha(
    #     quantifier_type='ALL',
    #     alpha_domain=(round(x, 2) for x in np.arange(0.8, 1.0, 0.01)),
    #     initial_temperature_domain=range(500, 10000, 500),
    #     threshold=1,
    #     num_simulations_in_each_batch=100,
    #     run_batch_kwargs=dict(min_set_size=5, max_set_size=61, number_of_pairs=50)
    # )
    heatmap_of_results('ALL', os.path.join('opt_grid', 'opt_temperature_and_alpha', 'ALL', 'grid_eval.csv'))
