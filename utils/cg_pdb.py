#!/usr/bin/env python

# omarin at 2017Apr25
# read a coarse-grained (only Calpha) pdb
# function to return residues within N amstrongs

import numpy as np


def read_cg_pdb(path):
    numbers = []
    positions = []
    with open(path) as f:
        for line in f:
            if line.startswith('ATOM'):
                stuff = line.split()
                numbers.append(stuff[1])
                positions.append(map(float, (stuff[-3], stuff[-2], stuff[-1])))

    return numbers, np.array(positions)


def residue_at_less_than(pdb, pdb_resi, cutoff=10):
    n = pdb_resi - 1
    npos = pdb[n]
    dist_vs_npos = lambda x: np.linalg.norm(x-npos)
    d_vs_n = np.apply_along_axis(dist_vs_npos, 1, pdb)
    tf = d_vs_n < cutoff
    close_people = [n for n, a in enumerate(tf.tolist()) if a]
    return map(lambda x: x+1, close_people)


if __name__ == '__main__':
    import sys
    n, pdb = read_cg_pdb(sys.argv[1])
    residue_at_less_than(pdb, 33)
