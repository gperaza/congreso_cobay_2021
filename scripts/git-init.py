#!/usr/bin/env python3

# Modified by Gonzalo Peraza 2020

# Script to init a git repo for a lesson template
# Assumes that cwd is the released assignment directory, under release

import os
import shutil
import subprocess


if __name__ == '__main__':
    template_dir = '/home/gperaza/Nbgrader/nbgrader-scripts/'

    readme_file = os.path.join(template_dir, 'README.md')
    shutil.copyfile(readme_file, os.path.join('.', 'README.md'))
    ignore_file = os.path.join(template_dir, 'gitignore')
    shutil.copyfile(ignore_file, os.path.join('.', '.gitignore'))

    subprocess.check_output(['git', 'init'])
    subprocess.check_output(['git', 'add', '-A'])
    subprocess.check_output(['git', 'commit', '-mFirst commit'])
