__author__ = 'Panagiotis Koukos'

"""
fuzznuc.py - Scan input files with fuzznuc.

This module scans the input files for the presence of the specified
nucleotide sequence and stores the results in an aptly named text file.

:param -i, --in: Path to the file which contains the sequences to parse.
:type -i, --in: str or unicode
:param -p, --pat: Path to the file which contains the pattern to use.
:type -p, --pat: str or unicode
:param -o, --out: What file to write the results in.
:type -o, --out: str or unicode
:return None
"""

# import argparse
import subprocess
import sys
import atexit

# From http://stackoverflow.com/a/11270665
try:
    from subprocess import DEVNULL  # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')


# TODO fix the repeating devnull import. Maybe use an exit function?
@atexit.register
def custom_exit():
    DEVNULL.close()


def check_fuzznuc():
    """
    Check for the presence of fuzznuc in the local system.

    This functions uses the linux built in command 'which' to
    check if the command fuzznuc is available.

    :param : none
    :return: The absolute path to the fuzznuc program as returned
             by which on success, None on failure.
    """

    try:
        # stdout=DEVNULL suppresses the output of the system call.
        # TODO Port this through python instead of which for compatibility?
        subprocess.check_call(['which', 'fuzznuc'], stdout=DEVNULL)
    except subprocess.CalledProcessError:
        print 'Unable to locate fuzznuc on the local system. Aborting.'
        custom_exit()
        return None

    fuzznuc = subprocess.check_output(['which', 'fuzznuc']).rstrip()
    return fuzznuc


def call_fuzznuc(fuzznuc, input_file, output_file, pattern, nof_mismatches):
    """
    Call fuzznuc with the specified arguments.

    :param fuzznuc: Full path to the fuzznuc binary, as found by check_fuzznuc.
    :type fuzznuc: str or unicode
    :param input_file: Path to the sequence (FASTA) file.
    :type input_file: str or unicode
    :param output_file: File in which fuzznuc will store its output.
    :type output_file: str or unicode
    :param pattern_file: Path to the file which contains the fuzznuc settings.
    :type pattern_file: str or unicode
    :return: None
    """

    if not output_file:
        output_file = input_file.split('.')[0] + '.fuzznuc'
        # print output_file

    try:
        subprocess.check_call([fuzznuc,
                               '-sequence', input_file,
                               '-pattern', pattern,
                               '-pmismatch', nof_mismatches,
                               '-outfile', output_file,
                               '-rformat', 'simple'],
                              stdout=DEVNULL,
                              stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        print 'One or more files not found. Aborting.'
        custom_exit()
        return None


# TODO: Write the __name__ == main wrapper so that this is usable as a module
# TODO: and a script too.
def main():
    call_fuzznuc(check_fuzznuc(), 'ERR145618_1.FASTA', '', 'TGTGGGGAAAAGCAAGAGAG', '2')

if __name__ == '__main__':
    main()