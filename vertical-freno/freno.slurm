#!/bin/bash

#SBATCH --mail-user=jz2915@nyu.edu
#SBATCH --mail-type=ALL
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=0-12:00
#SBATCH --mem=128G
#SBATCH --output=exp/slurm/freno.%j.out
#SBATCH --error=exp/slurm/freno.%j.err
#SBATCH --account=ogm2
#SBATCH --partition=debug

source /gpfsnyu/home/jz2915/config.sh

module purge
module load python/intel/3.6.6
python $script $expsnum $data $mem $result
