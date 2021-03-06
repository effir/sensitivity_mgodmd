#!/usr/bin/env python
# author: omarin

import os
import numpy as np
import utils.cg_pdb as cgpdb


def create_mutation_files(path_analysis, path_aln, path_ref_pdb, w, factor):

    l = []
    with open(path_aln) as f:
        # aln files are just lists of numbers.
        for line in f:
            number = line.strip()
            l.append(number)

    ll = len(l)
    # if we return to seq-based window
    #li = [a-w for a in xrange(ll)]
    #li = map(lambda x: 0 if x < 0 else x, li)
    #lj = [a+w for a in xrange(ll)]
    #lj = map(lambda x: ll if x+1 > ll else x, lj)

    resilist, pdb = cgpdb.read_cg_pdb(path_ref_pdb)
    for cat, value in zip(['plus', 'minus'], [factor*1.0, 1.0/factor]):
        cat_path = os.path.join(path_analysis, cat)

        for nl in xrange(ll):
            num = l[nl]
            cat_num = os.path.join(cat_path, num)
            os.mkdir(cat_num)
            cat_file = os.path.join(cat_num, 'mutation.dat')

            with open(cat_file, 'w') as f:
                #i = li[nl]
                #j = lj[nl]
                #printers = ['{}\t{}'.format(resi, value) for resi in l[i:j+1]]
                pdbnum = resilist[nl]
                close = cgpdb.residue_at_less_than(pdb, pdbnum, cutoff=w)
                printers = ['{}\t{}'.format(resi, value) for resi in close]
                f.write('\n'.join(printers))


def prepare_sensitivity(path, base_prot, obj_protein, refpdbpath, window=1, factor=10):
    basepath = os.path.abspath(path)
    files = os.listdir(path)

    for a in range(100):
        analysis_path = os.path.join(basepath, 'sensitivity')
        analysis_path += str(a)

        if os.path.isdir(analysis_path):
            continue
        else:
        # creating directory structure
            os.mkdir(analysis_path)
            more_energy = os.path.join(analysis_path, 'plus')
            os.mkdir(more_energy)
            less_energy = os.path.join(analysis_path, 'minus')
            os.mkdir(less_energy)
            break

    path_aln = os.path.join(path, '{}.aln'.format(base_prot))
    create_mutation_files(analysis_path, path_aln, refpdbpath, window, factor)

    exe = os.path.abspath('./launch_sensitivity.py')

    call = 'python {} {} {} {} {}'.format(exe, basepath, analysis_path, base_prot, obj_protein)

    return call
