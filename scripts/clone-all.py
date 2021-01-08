#!/usr/bin/env python3

# From: https://github.com/earthlab/autograding-notebooks/tree/master/scripts
# Modified by Gonzalo Peraza 2020

# Script to clone all student repos from a given GitHub classroom course
# and then copy over the assignment files into the nbgrader `submitted` dir
# Assumes that cwd is nbgrader course dir

import os
import glob
import shutil
import subprocess
import configparser
import pandas as pd


def mkdir_p(path):
    dirname = os.path.dirname(path)
    if dirname:
        mkdir_p(dirname)
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def clone_repo(assignment, github_username, classroom, clonedir,
               skip, dry_run):
    slug = "{}-{}".format(assignment, github_username)
    destdir = os.path.join(clonedir, slug) # path to repo

    if os.path.isdir(destdir):
        # if the repo already exists, pull (unless skip_existing)
        if skip:
            return
        cmd = ['git', '-C', destdir, 'pull']
        cmdargs = []
    else:
        url = "git@github.com:{}/{}.git".format(classroom, slug)
        # repo does not already exist; clone
        cmd = ['git', '-C', clonedir, 'clone']
        cmdargs = [url]
    if dry_run:
        cmd.append('--dry-run')
        print(cmd + cmdargs)
        return True
    return subprocess.call(cmd + cmdargs)


if __name__ == '__main__':
    # Most options are set on config file
    config = configparser.ConfigParser()
    config.read('gh_class_config')
    classroom = config['DEFAULT']['classroom']
    roster = config['DEFAULT']['roster']
    clonedir = config['DEFAULT']['clonedir']

    roster = pd.read_csv(roster,
                         usecols=('identifier',
                                  'github_username')).set_index('identifier')

    # argument parsing
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--assignment', required=True)
    parser.add_argument('-n', '--dry-run',
                        help='List repositories that would be cloned',
                        action='store_true')
    parser.add_argument('--skip-existing',
                        help='Skip repositories that have already been cloned',
                        action='store_true')
    args = parser.parse_args()
    assignment = args.assignment
    skip = args.skip_existing
    dry_run = args.dry_run

    missing = []
    mkdir_p(clonedir)

    for identikey, (github_username,) in roster.iterrows():
        slug = "{}-{}".format(assignment, github_username)
        if clone_repo(assignment, github_username, classroom, clonedir,
                      skip, dry_run):
            missing.append((identikey, github_username))
        else:
            notebooks = glob.glob(os.path.join(clonedir, slug, '*.ipynb'))
            scripts = glob.glob(os.path.join(clonedir, slug, '*.py'))
            directories = ['data', 'images', 'Data', 'Figures']
            dest = os.path.join('submitted', identikey, assignment)
            if os.path.isdir(dest):
                shutil.rmtree(dest)
            mkdir_p(dest)
            for f in notebooks + scripts:
                print("copying {} to {}".format(f, dest))
                shutil.copy(f, dest)
            for d in directories:
                d2 = os.path.join(clonedir, slug, d)
                if os.path.isdir(d2):
                    print("copying {} to {}".format(d, dest))
                    shutil.copytree(d2, os.path.join(dest, d))

    if len(missing) == 0:
        print('All successful; no missing repos')
    else:
        print('Missing repositories: ', missing)
