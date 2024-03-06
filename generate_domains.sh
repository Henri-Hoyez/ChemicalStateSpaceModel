#/bin/bash

script_to_ececute=("time_shift.py" "input_noise.py" "output_noise.py" "shift_in_mean.py" "non_linear_injective.py" "non_linear_surjective.py" "causal_shift.py" "shift_in_unit.py" "amplitude_shift.py" "frequency_shift.py")
# script_to_ececute=("shift_in_mean.py" "time_shift.py")
n_strengths=10
save_folder="ssm_dataset"

#  Generate the source domain
echo generate the source domain...
python generate_source.py "${save_folder}/01 - Source Domain.h5"


for script in "${script_to_ececute[@]}" 
do
    domain_shift_type=(${script//./ })
    echo saving to ${save_folder}"/"${domain_shift_type}"/"...

    for (( s=0; s<n_strengths; s++ )) 
    do
        echo executing $script "--strength" $s "..."
        python ${script} ${save_folder}"/"${domain_shift_type}"/" --strength $s

    done
done






