#!/usr/bin/env python

#  test call mgodmd in cluster
#  one job (with one core) for protein
#  right now --> calls jobs inside script iteratively
#  may update code to use more resources if needed
#  author: omarin

# call as:
# python sensitivity_analysis_slurm.py
# path_to_param_file
#       param_file: initial_prot,target_prot,path_to_directory
#       with a line for each intended sensitivity analysis
# queue[
#       right now should be TITAN]
# factor[
#       factor by which we modify the residue potential..
#       ..max 100, more than that NOT supported by GOdMD]
# window[
#       num of aa touched by factor of /factor/]


import os
import sys
import subprocess
import prepare_mgodmd as pmd


def read_params(path):
    # key for each ref_prot, value for its associated directory
    if not(os.path.isfile(path)):
        print("Unable to find config file {}")
        print("python ")
        exit(-1)

    d = {}
    with open(path) as f:
        for line in f:
            ref, obj, path, cgpdbname = line.strip().split(',')
            d[ref] = (obj, path, os.path.join(path, cgpdbname))
    return d


def prepare_sbatch(path, protein, objprotein, cgpdbpath, q, factor, window):
    for a in range(100):
        batch_file = '{}{}.sh'.format(protein, a)
        if os.path.isfile(batch_file):
            continue
        n = a
        break

    command = pmd.prepare_sensitivity(path, protein, objprotein, cgpdbpath, window=window, factor=factor)

    if not command:
        # some mistake on prepare_sensitivity
        # error message should be already given
        return 0

    name = '{}{}'.format(protein, n)
    with open(batch_file, 'w') as f:
        f.write("""#!/bin/bash
#SBATCH -p {0}
#SBATCH -J {1}
#SBATCH -o {1}.out
#SBATCH -e {1}.err

module load python-2.7.3

{2}""".format(q, name, command))

    return batch_file


def main(param, queue, factor, window):
    d = read_params(param)

    factor = float(factor)
    if factor > 100:
        print("Maximum available factor is 100")
        exit()

    window = int(window)

    for k in d.keys():
        obj, path, cgpdbpath = d[k]
        if not(os.path.isdir(path)):
            print('path {} for protein {} not found'.format(path, k))
            continue

        runner = prepare_sbatch(path, k, obj, cgpdbpath, queue, factor, window)
        if not runner:
            continue
        subprocess.call(['sbatch', runner])


if __name__ == '__main__':
    main(*sys.argv[1:])
