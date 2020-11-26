#!/bin/bash

#SBATCH --mail-user=jz2915@nyu.edu
#SBATCH --mail-type=ALL
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=0-10:00
#SBATCH --mem=64G
#SBATCH --output=exp/slurm/canTree.%j.out
#SBATCH --error=exp/slurm/canTree.%j.err
#SBATCH --account=ogm2
#SBATCH --partition=debug

source /gpfsnyu/home/jz2915/config.sh

module purge
module load python/intel/3.6.6
python $script $expsnum $data $perf $result
