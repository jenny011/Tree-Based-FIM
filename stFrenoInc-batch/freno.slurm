#!/bin/bash

#SBATCH --mail-user=jz2915@nyu.edu
#SBATCH --mail-type=ALL
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=0-12:00
#SBATCH --mem=128G
#SBATCH --output=slurm/%j.out
#SBATCH --error=slurm/%j.err
#SBATCH --account=ogm2
#SBATCH --partition=debug

source /gpfsnyu/home/jz2915/centralized/config.sh

module purge
#module load python/intel/3.6.6
module load anaconda3/5.2.0
python $runperf $expsnum $data $perf $re
