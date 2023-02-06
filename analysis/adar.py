from Bio import SeqIO
from pathlib import Path
import os
import pandas as pd
from argparse import ArgumentParser


def get_args():
    """Get arguments from the command line.
    """
    parser = argparse.ArgumentParser(
                    prog = 'editFinder',
                    description = 'What the program does',
                    epilog = 'Text at the bottom of help')
    parser.add_argument()

    args = parser.parse_args()

    return args


class trace():
    """Class which represents individual Sanger sequence trace (ab1 files).
    """

    def __init__(self, ab1_path, expected_conversion, output_dir):
        self.ab1_path = Path(ab1_path)
        self.expected_conversion = expected_conversion
        self.output_dir = Path(output_dir)
    
    @property
    def basecall_file(self):
        return f'{self.output_dir.joinpath(self.ab1_path.stem)}.tracy.basecalls.tsv'
    

    def _tracy_basecall(self):
        """Use Tracy to generate basecalls from the provided abi file. Since
        we are lazy for now assume that Tracy is globally available.

        After the basecalls are saved to a tsv file read and return the results as
        a pandas dataframe.
        """

        cmd = f"tracy basecall -f tsv -o {str(self.basecall_file)} {str(self.ab1_path)}"
        os.system(cmd)


        return pd.DataFrame(self.basecall_file, sep='\t')
    

    def identify_edits(self):
        """This method is really the core functionality of the script. The idea being we will use
        the relative signal that is included as part of the Tracy basecalls in order to locate
        bases where editing may have occurred in some population of the molecules present in the
        Sanger sequencing reaction. 
        """

        # Call bases using Tracy
        basecalls = self._tracy_basecall()

        # ab1 files include 10 values per base. Tracy retains those values which is nice but to
        # simplify we will throw out rows that are not assigned to a nucleotide position. The
        # sites that are retained should be the peak crests

        bc_trim = basecalls.loc[basecalls['basenum'] != 'NA']

        assert len(bc_trim) > 0

        





def main():

    pass
