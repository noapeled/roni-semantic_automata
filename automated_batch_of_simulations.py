from multiprocessing.pool import Pool
from run_single_simulation import run_single_simulation


def run_single_simulation_for_multiprocessing(args_and_kwargs):
    args, kwargs = args_and_kwargs
    return run_single_simulation(*args, **kwargs)


if __name__ == '__main__':
    pool = Pool(processes=2, maxtasksperchild=1)
    # itr = pool.imap_unordered(run_single_simulation_for_multiprocessing,
    #                           [(('EXACTLY', 2000, 1.0, 0.95),
    #                            dict(
    #                                    ns=(2, 5, 9), min_sample_for_each_n=5, max_sample_for_each_n=10,
    #                                    min_zeros_per_positive_example=0, max_zeros_per_positive_example=20))] * 2)
    # itr = pool.imap_unordered(run_single_simulation_for_multiprocessing,
    #                           [(('ALL', 2000, 1.0, 0.95),
    #                            dict(min_set_size=5, max_set_size=61, number_of_pairs=50))] * 8)
    itr = pool.imap_unordered(run_single_simulation_for_multiprocessing,
                              [(('ALL_OF_THE_EXACTLY', 2000, 1.0, 0.95),
                               dict(ns=(2, 5, 9), min_sample_for_each_n=5, max_sample_for_each_n=10))] * 8)
    for run_return_value in itr:
        print('Finished run, return value is:\n%s' % run_return_value)
