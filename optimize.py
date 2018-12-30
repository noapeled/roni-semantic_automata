import pickle
from automated_batch_of_simulations import run_batch
from functools import partial
from GPyOpt.methods import BayesianOptimization


def f_optimize_all(params, alpha, threshold, num_simulations, run_batch_kwargs):
    total_success = run_batch(
        base_seed=0,
        quantifier_type='ALL',
        initial_temperature=params[:, 0],
        threshold=threshold,
        alpha=alpha,
        num_simulations=num_simulations,
        **run_batch_kwargs)
    return total_success / float(num_simulations)


def optimize(alpha, threshold, num_simulations_in_each_batch, run_batch_kwargs):
    bayes_opt = BayesianOptimization(
        maximize=True,
        f=partial(f_optimize_all,
                  alpha=alpha,
                  threshold=threshold,
                  num_simulations=num_simulations_in_each_batch,
                  run_batch_kwargs=run_batch_kwargs),
        domain=[
            dict(name='initial_temperature', type='continuous', domain=(1, 10000)),
        ])
    bayes_opt.run_optimization(max_iter=15,
                               verbosity=True,
                               report_file='opt_report.txt',
                               evaluations_file='opt_evaluations.txt',
                               models_file='opt_models.txt')
    pickle.dump(bayes_opt, 'bayes_opt.pkl')


if __name__ == '__main__':
    optimize(alpha=0.96,
             threshold=1,
             num_simulations_in_each_batch=100,
             run_batch_kwargs=dict(min_set_size=5, max_set_size=61, number_of_pairs=50))
