import os
import subprocess
import logging


class GTDBTkUtils():
    '''
    Utilities for running GTDB-Tk
    '''

    def __init__(self, config, callback_url, workspace_id, cpus):
        self.shared_folder = config['scratch']
        self.callback_url = callback_url
        self.cpus = cpus
        self.gtdbtk = '/bin/bash -c "source activate py2 && GTDBTK_DATA_PATH=/data gtdbtk'
        logger = logging.getLogger(__name__)

    def gtdbtk_classifywf(self, fasta_paths):
        '''
        Run the classify workflow on the fasta files
        '''
        out_dir = os.path.join(self.shared_folder, "output")
        gtdbtk_cmd = " ".join([self.gtdbtk, "classify_wf", "--out_dir", out_dir,
                              "--genome_dir", self.shared_folder, "-x", "fa",
                               "--cpus", str(self.cpus), '"'])
        logger.info("Starting Command:\n" + gtdbtk_cmd)
        output = subprocess.check_output(gtdbtk_cmd, shell=True).decode('utf-8')
        logger.info(output)

        for path in (os.path.join(out_dir, 'gtdbtk.ar122.summary.tsv'),
                     os.path.join(out_dir, 'gtdbtk.bact120.summary.tsv')):
            try:
                summary_file = open(path, 'r')
                output = output + summary_file.read()
                summary_file.close()
            except Exception as exc:
                logger.info(exc)

        return output
