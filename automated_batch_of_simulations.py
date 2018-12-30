import os
import uuid
from printer import info, set_up_logging
from multiprocessing.pool import Pool
from run_single_simulation import SingleSimulationRunner, run_dir


def run_single_simulation_for_multiprocessing(args_and_kwargs):
    args, kwargs = args_and_kwargs
    seed, args_for_simulation = args[0], args[1:]
    set_up_logging('out.log')
    info('##### Task is:', args_and_kwargs)
    return SingleSimulationRunner(seed).run_single_simulation(*args_for_simulation, **kwargs)


def run_batch(base_seed,
              quantifier_type, initial_temperature, threshold, alpha,
              num_simulations,
              **kwargs):
    tasks = [((seed, quantifier_type, initial_temperature, threshold, alpha), kwargs)
             for seed in range(base_seed, base_seed + num_simulations)]
    with Pool(maxtasksperchild=1) as pool:
        results = pool.map(run_single_simulation_for_multiprocessing, tasks)
        total_success = sum(results)
        info('########### Total success for quantifier %s is %d of %d' % (quantifier_type, total_success, num_simulations))
        with open(os.path.join(run_dir(quantifier_type, initial_temperature, alpha, threshold), 'num_success.csv'), 'w') as f_num_success:
            f_num_success.write('percent_success,total_success,num_simulations,quantifier,base_seed\n%f,%d,%d,%s,%s\n' %
                                (total_success / float(num_simulations), total_success, num_simulations, quantifier_type, base_seed))
        return total_success


if __name__ == '__main__':
    # ============> FOR REPRODUCIBILITY, YOU MUST SET PYTHONHASHSEED=0 IN ENV BEFORE RUNNING <==========
    set_up_logging('out.log')
    base_seed = uuid.uuid1().int
    info('-------------- STARTING BATCH OF SIMULATIONS WITH BASE SEED %s ---------' % base_seed)

    run_batch(base_seed, 'ALL', 700, 1.0, 0.96,
              num_simulations=3,
              min_set_size=5, max_set_size=61, number_of_pairs=50)

    # run_batch(base_seed, 'NONE', 1500, 1.0, 0.93,
    #      num_simulations=10,
    #      min_set_size=5,
    #      max_set_size=61,
    #      number_of_pairs=50)
    #
    # run_batch(base_seed, 'BETWEEN_WITH_FIXED_UNIVERSE_SIZE', 2000, 1.0, 0.95,
    #      num_simulations=10,
    #      all_ones=[],
    #      at_least_ones=3, at_most_plus_1_ones=6, fixed_universe_size=10,
    #      number_of_positive_examples=50)
    #
    # run_batch(base_seed, 'BETWEEN_WITH_DYNAMIC_UNIVERSE_SIZE', 2500, 1.0, 0.95,
    #      num_simulations=10,
    #      add_examples_which_are_all_ones_of_these_lengths=[],
    #      at_least_ones=5, at_most_ones=61, min_size_of_universe=20,
    #      max_size_of_universe=80, number_of_positive_examples=50)
    #
    # run_batch(base_seed, 'EXACTLY', 3700, 1.0, 0.96,
    #      num_simulations=10,
    #      ns=(2, 5, 9),
    #      min_sample_for_each_n=5,
    #      max_sample_for_each_n=10,
    #      min_zeros_per_positive_example=0,
    #      max_zeros_per_positive_example=20)
    #
    # run_batch(base_seed, 'ALL_OF_THE_EXACTLY', 3800, 1.0, 0.97,
    #      num_simulations=10,
    #      ns=(2, 5, 9), min_sample_for_each_n=5, max_sample_for_each_n=10)

    info('-------------- FINISHED BATCH OF SIMULATIONS WITH BASE SEED %s ---------' % base_seed)
