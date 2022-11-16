#!/bin/bash

#BATCH -J SAMPLE_JOB     # job name
#SBATCH -o log_slurm.o%j  # output and error file name (%j expands to jobID)
#SBATCH -N 1              # number of nodes you want to run on
#SBATCH -n 1             # total number of tasks requested
#SBATCH -p defq         # queue (partition) -- defq, eduq, gpuq, shortq
#SBATCH -t 24:00:00       # run time (hh:mm:ss) - 12.0 hours in this example.

# Generally needed modules:
module load slurm
# module load python/intel

# Execute the program:
python --version
mpirun /home/loganscamfer/.conda/envs/Research/bin/python /home/loganscamfer/2022-Infrasound-Python/python_scripts/Infrasound_Array_Processing_24hrs.py

## Some examples:
# mpirun python3 script.py

# Exit if mpirun errored:
status=$?
if [ $status -ne 0 ]; then
    exit $status
fi

