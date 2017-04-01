from multiprocessing.pool import Pool
from run_single_simulation import run_single_simulation


def run_single_simulation_for_multiprocessing(args_and_kwargs):
    args, kwargs = args_and_kwargs
    return run_single_simulation(*args, **kwargs)


def main(quantifier_type, initial_temperature, threshold, alpha,
         num_simulations,
         num_processes=2,
         **kwargs):
    pool = Pool(processes=num_processes, maxtasksperchild=1)
    itr = pool.imap_unordered(run_single_simulation_for_multiprocessing,
                              [((quantifier_type, initial_temperature, threshold, alpha),kwargs)] * num_simulations)
    for run_return_value in itr:
        print('Finished run, return value is:\n%s' % run_return_value)


if __name__ == '__main__':
    main('NONE', 2000, 1.0, 0.95,
         num_simulations=1,
         min_set_size=5,
         max_set_size=61,
         number_of_pairs=50)

    # main('EXACTLY', 2000, 1.0, 0.95,
    #      num_simulations=1,
    #      ns=(2, 5, 9),
    #      min_sample_for_each_n=5,
    #      max_sample_for_each_n=10,
    #      min_zeros_per_positive_example=0,
    #      max_zeros_per_positive_example=20)

    # main('ALL', 2000, 1.0, 0.95,
    #      num_simulations=10,
    #      min_set_size=5, max_set_size=61, number_of_pairs=50)

    # main('ALL_OF_THE_EXACTLY', 2000, 1.0, 0.95,
    #      num_simulations=10,
    #      ns=(2, 5, 9), min_sample_for_each_n=5, max_sample_for_each_n=10)

    # main('BETWEEN_WITH_FIXED_UNIVERSE_SIZE', 2000, 1.0, 0.95,
    #      num_simulations=10,
    #      all_ones=[],
    #      at_least_ones=3, at_most_plus_1_ones=6, fixed_universe_size=10,
    #      number_of_positive_examples=50)
