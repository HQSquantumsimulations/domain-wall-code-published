import glob, os
import json
import numpy as np
import re
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt 

CODE_NAME = "XXXZZZ"
colours = ["pink","blue", "green", "red", "purple", "black","orange"]

def filter(data, filter_dict):
    
    df = data.copy()
    
    for key, value in filter_dict.items():
    
        mask = df[key] == value
        df = df[mask]

    return df

def merge_json_files(directory):

    output_dict = dict()

    cwd = os.getcwd()
    os.chdir(directory)
    run_data = []
    print("Merge json files")
    for file in tqdm(glob.glob("*.json")):
        # print(file)
        f = open(file)
        r = json.load(f)

        for run in r:
            run["n"] = run['n_k_d'][0]
            run['k'] = run['n_k_d'][1]
            run['d'] = run['n_k_d'][2]
            # print(re.search('bias=(.*),', run['error_model']))
            run['bias'] = float(re.search('bias=(.*),', run['error_model']).group(1))
            if run['bias'] == 0: run['bias'] = 0.5
            run['decoder_chi'] = float(re.search('\(chi=(.*?)\)', run['decoder']).group(1))
            run['n_k_d'] = repr(run['n_k_d'])

            run_data.append(pd.DataFrame.from_dict(run))

            # print(f"[[{run['n']},{run['k']},{run['d']}]], Bias = {run['bias']}, Chi = {run['decoder_chi']}")


    run_data = pd.concat(run_data)

    return run_data

if __name__ == "__main__":
    data = merge_json_files("chi_tests")
    
    plt.figure()
    for i,chi in enumerate([12,18,24,30,36]):

        lers = []
        biases = []

        for bias in [0.5,1,3,10,30,100,300,1000]:

            filtered_data = filter(data, {"decoder_chi": 36, "bias": bias})
            n_run = filtered_data['n_run'].sum()
            n_success = filtered_data['n_success'].sum()
            pL = 1 - n_success/n_run
            pL_eb = np.sqrt(pL*(1-pL)/n_run)
            pL36 = pL

            filtered_data = filter(data, {"decoder_chi": chi, "bias": bias})
            n_run = filtered_data['n_run'].sum()
            n_success = filtered_data['n_success'].sum()
            pL = 1 - n_success/n_run
            pL_eb = np.sqrt(pL*(1-pL)/n_run)

            # plt.scatter(bias,abs(pL-pL36),label=f"chi={chi}")

            biases.append(bias)
            lers.append(pL-pL36)

            print(f"Bias = {bias}, Chi = {chi}, dpL = {pL-pL36}")

        plt.scatter(biases,lers,label=f"chi={chi}", marker = "_", s = 500, linewidth = 4)


    plt.legend()
    plt.xscale('log')

    plt.xlabel("Bias")
    plt.ylabel("f(chi)-f(chi=36)")
    plt.title("Chi dependence. Distance-19 color code.\nPhysical error ~ at the threshold for given bias.")
    # plt.yscale('log')
    plt.show()
    plt.savefig("chi.png")


    # codes = list(set(codes))
    # error_models = list(set(error_models))

    # for model in error_models:
    #     data_f1 = filter(run_data, 'error_model', model)
    #     output_dict[model] = dict()
    #     for code in codes:
    #         output_dict[model][code] = dict()
    #         data_f2 = filter(data_f1, "n_k_d", code)
            
    #         probs = []
    #         for data_point in data_f2:
    #             # answer = str(round(answer, 2))
    #             probs.append(data_point['error_probability'])

    #         probs = list(set(probs))
    #         probs.sort()
    #         for prob in probs:
    #             data_f3 = filter(data_f2, 'error_probability', prob)
    #             output_dict[model][code][prob]= dict()
    #             n_run = 0
    #             n_success = 0
    #             n_fail = 0
    #             for data in data_f3:
    #                 n_run+=data["n_run"]
    #                 n_success+=data["n_success"]
    #                 n_fail+=data["n_fail"]
    #                 distance = data["distance"]


    #             output_dict[model][code][prob]['n_run'] = n_run
    #             output_dict[model][code][prob]['n_success'] = n_success
    #             output_dict[model][code][prob]['n_fail'] = n_fail
    #             output_dict[model][code][prob]['distance'] = distance
    #             pL=n_fail/n_run
    #             output_dict[model][code][prob]['logical_failure_rate'] = pL
    #             output_dict[model][code][prob]['logical_failure_rate_error_bar'] = np.sqrt(pL*(1-pL)/n_run)

    # # os.chdir(cwd)
    # return output_dict

