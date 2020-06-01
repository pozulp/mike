#!/usr/bin/env python
'''
Convrt rtf files in cwd to txt using unrtf such that the git log --follow
history of the files is preserved. This requires two commits. The first
renames the files from .rtf to .txt and the second converts them with unrtf.
'''

import glob
import os

def rename(filenames):
    for fname in filenames:
        os.system(f'git mv {fname}.rtf {fname}.txt')

    os.system('git commit -m "Renamed .rtf recipes to .txt"')

def convert(filenames):
    for fname in filenames:
        os.system(f'unrtf --text --quiet {fname}.txt > {fname}.txt.unrtf')
        os.system(f'mv {fname}.txt.unrtf {fname}.txt')

    os.system('git commit -a -m "Convert rtf recipes to text using unrtf"')


if __name__ == '__main__':
    filenames = [os.path.splitext(x)[0] for x in glob.glob('*.rtf')]
    rename(filenames)
    response = input('Please adjust index.html. All done? [y/n] ')
    if response.lower() == 'y':
        convert(filenames)
