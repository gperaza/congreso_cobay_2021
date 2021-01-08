#!/usr/bin/env python3

# From: https://github.com/earthlab/autograding-notebooks/tree/master/scripts
# Modified by Gonzalo Peraza 2020

# Script to copy nbgrader html feedback reports to feedback.html in student
# repos and push repos to github
# Assumes that cwd is nbgrader course dir

import os
import glob
import shutil
import subprocess
import configparser
import pandas as pd


def run_cmd(cmd, cmdargs, dry_run):
    if (dry_run):
        cmdargs.insert(1, '--dry-run')
        print(cmd+cmdargs)
    # note that commit when there aren't any changes will produce a
    # non-zero exit code (even with dry-run)
    subprocess.check_output(cmd + cmdargs)


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
    args = parser.parse_args()
    assignment = args.assignment
    dry_run = args.dry_run

    for identikey, (github_username,) in roster.iterrows():
        try:
            html_list = glob.glob(os.path.join('feedback',
                                               identikey, assignment,
                                               '*.html'), recursive=True)
            if len(html_list) < 1:
                print("No feedback found for {},{}".format(identikey, assignment))
                continue

            # (source,) = glob.glob(os.path.join('feedback',
            #                                    identikey, assignment,
            #                                    '*.html'), recursive=True)
        except ValueError:
            # Lack of feedback usually means student did not submit homework
            print("No feedback found for {},{}".format(identikey, assignment))
            continue

        slug = "{}-{}".format(assignment, github_username)
        destdir = os.path.join(clonedir, slug)
        dest_list = []
        for i in range(len(html_list)):
            dest_list.append(os.path.join(destdir, f'feedback_{i+1}.html'))
        if os.path.exists(destdir):
            for source, dest in zip(html_list, dest_list):
                print("Copying feedback from {} to {}".format(source, dest))
                shutil.copyfile(source, dest)
        else:
            print('Destination directory does not exist: {}'.format(destdir))

        gitcmd = ['git', '-C', destdir]
        try:
            # add
            cmdargs = ['add', os.path.basename(dest)]
            run_cmd(gitcmd, cmdargs, dry_run)
            # commit
            cmdargs = ['commit', '-mAdd feedback.html']
            run_cmd(gitcmd, cmdargs, dry_run)
            # push
            cmdargs = ['push']
            run_cmd(gitcmd, cmdargs, dry_run)
        except subprocess.CalledProcessError as e:
            print(e.output)
            print('Skipping {}'.format(destdir))
