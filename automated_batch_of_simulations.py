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
                              [((quantifier_type, initial_temperature, threshold, alpha), kwargs)] * num_simulations)
    total_success = 0
    for i, run_return_value in enumerate(itr):
        print('Finished run %d of %d, return value is: %s' % (i + 1, num_simulations, run_return_value))
        total_success += run_return_value
    print('########### Total success for quantifier %s is %d of %d' % (quantifier_type, total_success, num_simulations))
    return total_success


if __name__ == '__main__':
    # main('ALL', 1500, 1.0, 0.91,
    #      num_simulations=1,
    #      min_set_size=5, max_set_size=61, number_of_pairs=50)
    #
    # main('NONE', 1500, 1.0, 0.93,
    #      num_simulations=1,
    #      min_set_size=5,
    #      max_set_size=61,
    #      number_of_pairs=50)

    # main('BETWEEN_WITH_FIXED_UNIVERSE_SIZE', 2000, 1.0, 0.95,
    #      num_simulations=1,
    #      all_ones=[],
    #      at_least_ones=3, at_most_plus_1_ones=6, fixed_universe_size=10,
    #      number_of_positive_examples=50)
    #
    # main('BETWEEN_WITH_DYNAMIC_UNIVERSE_SIZE', 2500, 1.0, 0.95,
    #      num_simulations=1,
    #      add_examples_which_are_all_ones_of_these_lengths=[],
    #      at_least_ones=5, at_most_ones=61, min_size_of_universe=20,
    #      max_size_of_universe=80, number_of_positive_examples=50)

    # main('EXACTLY', 3700, 1.0, 0.96,
    #      num_simulations=1,
    #      ns=(2, 5, 9),
    #      min_sample_for_each_n=5,
    #      max_sample_for_each_n=10,
    #      min_zeros_per_positive_example=0,
    #      max_zeros_per_positive_example=20)
    #
    main('ALL_OF_THE_EXACTLY', 3800, 1.0, 0.97,
         num_simulations=10,
         ns=(2, 5, 9), min_sample_for_each_n=5, max_sample_for_each_n=10)
