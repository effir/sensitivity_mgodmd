#!/usr/bin/env python
# author: omarin

import sys
import os
import subprocess


def void_caller(path, call, ref_prot, obj_prot):
    for a in os.listdir(path):
        print('Analyzing {}'.format(a))  # debug 1
        num_dir = os.path.join(path, a)
        mut = '{}/mutation.dat'.format(num_dir)
        out = '{}/mut_traj.log'.format(num_dir)
        trj = '{}/mut_traj.crd'.format(num_dir)
        en = '{}/ener.dat'.format(num_dir)
        call_mut = call + ['-touch', mut, '-ener', en, '-trj', trj, '-o', out]
        print('Calling {}'.format(call_mut))  # debug 2
        subprocess.call(call_mut)
        if os.path.isfile('gmon.out'):
            os.remove('gmon.out')


def main(base, analysis_path, ref_prot, obj_prot):
    files = os.listdir(base)
    pdbs = [a for a in files if a.endswith('.pdb')]

    for a in pdbs:
        if a.startswith(ref_prot) and (a.find('REF') != -1):
            refpdb = os.path.join(base, a)
        elif a.startswith(ref_prot):
            pdb_a = os.path.join(base, a)
        elif a.startswith(obj_prot):
            pdb_b = os.path.join(base, a)

    alns = [a for a in files if a.endswith('.aln')]
    for a in alns:
        if a.startswith(ref_prot):
            aln_a = os.path.join(base, a)
        elif a.startswith(obj_prot):
            aln_b = os.path.join(base, a)

    exe = '../mutated-godmd/exe/godmd'
    param = os.path.join(base, 'param.in')
    if not os.path.isfile(param):
        print('No param file param.in')
        exit(-1)
    basecall = [exe, '-i', param, '-pdbin', pdb_a, '-pdbtarg', pdb_b,
            '-p1', aln_a, '-p2', aln_b]

    plus = os.path.join(analysis_path, 'plus')
    void_caller(plus, basecall, ref_prot, obj_prot)
    minus = os.path.join(analysis_path, 'minus')
    void_caller(minus, basecall, ref_prot, obj_prot)


if __name__ == '__main__':
    main(*sys.argv[1:])
