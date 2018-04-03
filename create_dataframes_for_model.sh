#!/bin/sh
#$-S /bin/sh
#$ -V

#$ -l h_vmem=50G
#$ -l h_rt=02:00:00

#$ -o /mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby
#$ -e /mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby

module load general/python/2.7.10
module load utilities/anaconda/2.5.0
source activate ukbb2
python /mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/create_dataframes_for_model.py

