#!/bin/sh
#$-S /bin/sh
#$ -M toby.wise@kcl.ac.uk
#$ -m ae
#$ -V


#$ -l h_vmem=50G

#$ -o /mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby
#$ -e /mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby

#export MKL_NUM_THREADS=4
#export NUMEXPR_NUM_THREADS=
#export OMP_NUM_THREADS=4

module load general/python/2.7.10
module load utilities/anaconda/2.5.0
source activate ukbb2
python /mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/adversity_prediction.py

