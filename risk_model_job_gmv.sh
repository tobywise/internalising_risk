#!/bin/sh
#$-S /bin/sh
#$ -M toby.wise@kcl.ac.uk
#$ -m ae
#$ -V

#$ -l h_vmem=100G
#$ -l h_rt=6:30:00

#$ -o /mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby
#$ -e /mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby

module load general/python/2.7.10
module load utilities/anaconda/2.5.0
source activate ukbb2
python /mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/adversity_genetic_risk_model_gmv.py

