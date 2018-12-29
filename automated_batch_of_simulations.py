import uuid
from printer import info, set_up_logging
from functools import partial
# from multiprocessing.pool import Pool
from run_single_simulation import SingleSimulationRunner


# def run_single_simulation_for_multiprocessing(args_and_kwargs):
#     args, kwargs = args_and_kwargs
#     seed, args_for_simulation = args[0], args[1:]
#     set_up_logging('out.log')
#     return SingleSimulationRunner(seed).run_single_simulation(*args_for_simulation, **kwargs)


def main(base_seed,
         quantifier_type, initial_temperature, threshold, alpha,
         num_simulations,
         # num_processes=2,
         **kwargs):
    # pool = Pool(processes=num_processes, maxtasksperchild=1)
    total_success = 0
    for i, seed in enumerate(range(base_seed, base_seed + num_simulations)):
        info('##### Task is:', (seed, quantifier_type, initial_temperature, threshold, alpha), kwargs)
        success = SingleSimulationRunner(seed)\
            .run_single_simulation(quantifier_type, initial_temperature, threshold, alpha, **kwargs)
        info('Finished run %d of %d, return value is: %s' % (i + 1, num_simulations, success))
        total_success += success
    info('########### Total success for quantifier %s is %d of %d' % (quantifier_type, total_success, num_simulations))
    return total_success


if __name__ == '__main__':
    set_up_logging('out.log')
    base_seed = uuid.uuid1().int
    info('-------------- STARTING BATCH OF SIMULATIONS WITH BASE SEED %s ---------' % base_seed)

    main(base_seed, 'ALL', 1500, 1.0, 0.91,
         num_simulations=10,
         min_set_size=5, max_set_size=61, number_of_pairs=50)

    # main(base_seed, 'NONE', 1500, 1.0, 0.93,
    #      num_simulations=10,
    #      min_set_size=5,
    #      max_set_size=61,
    #      number_of_pairs=50)
    #
    # main(base_seed, 'BETWEEN_WITH_FIXED_UNIVERSE_SIZE', 2000, 1.0, 0.95,
    #      num_simulations=10,
    #      all_ones=[],
    #      at_least_ones=3, at_most_plus_1_ones=6, fixed_universe_size=10,
    #      number_of_positive_examples=50)
    #
    # main(base_seed, 'BETWEEN_WITH_DYNAMIC_UNIVERSE_SIZE', 2500, 1.0, 0.95,
    #      num_simulations=10,
    #      add_examples_which_are_all_ones_of_these_lengths=[],
    #      at_least_ones=5, at_most_ones=61, min_size_of_universe=20,
    #      max_size_of_universe=80, number_of_positive_examples=50)
    #
    # main(base_seed, 'EXACTLY', 3700, 1.0, 0.96,
    #      num_simulations=10,
    #      ns=(2, 5, 9),
    #      min_sample_for_each_n=5,
    #      max_sample_for_each_n=10,
    #      min_zeros_per_positive_example=0,
    #      max_zeros_per_positive_example=20)
    #
    # main(base_seed, 'ALL_OF_THE_EXACTLY', 3800, 1.0, 0.97,
    #      num_simulations=10,
    #      ns=(2, 5, 9), min_sample_for_each_n=5, max_sample_for_each_n=10)

    info('-------------- FINISHED BATCH OF SIMULATIONS WITH BASE SEED %s ---------' % base_seed)
