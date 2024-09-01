import glob, os
import json
import numpy as np
import re
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt 
import matplotlib.colors as mcolors
from scipy.optimize import curve_fit

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
        try:
            r = json.load(f)
        except json.decoder.JSONDecodeError:
            print(f"Error loading file {file}. Ignoring ...")

        for run in r:
            run["n"] = run['n_k_d'][0]
            run['k'] = run['n_k_d'][1]
            run['d'] = run['n_k_d'][2]
            # print(re.search('bias=(.*),', run['error_model']))
            # run['bias'] = float(re.search('bias=(.*),', run['error_model']).group(1))
            run['bias'] = np.inf
            if run['bias'] == 0: run['bias'] = 0.5
            run['decoder_chi'] = float(re.search('\(chi=(.*?)\)', run['decoder']).group(1))
            run['n_k_d'] = repr(run['n_k_d'])

            run_data.append(pd.DataFrame.from_dict(run))

            # print(f"[[{run['n']},{run['k']},{run['d']}]], Bias = {run['bias']}, Chi = {run['decoder_chi']}, p = {run['error_probability']}")


    run_data = pd.concat(run_data)
    os.chdir(cwd)

    return run_data


# the function we are fitting to
def threshold_fit(variables, B0, B1, B2, mu, pth):
    # print(variables)
    #[B0, B1, B2, mu, pth] are the parematers to be fitted
    p, L = variables #p= physical error rate, L=distance
    return B0 + B1*(p - pth)*pow(L, 1 / mu) + B2*pow((p - pth)*pow(L, 1 / mu), 2)

if __name__ == "__main__":
    data = merge_json_files("thresholds/raw_data12")
    merge_file = open("thresholds/raw_data_merged12.csv","w+")
    data.to_csv(merge_file) 


    # exit(22)  
    
    # data1 = pd.read_csv("thresholds/raw_data_merged7.csv")
    # data2 = pd.read_csv("thresholds/raw_data_merged2.csv")
    # data4 = pd.read_csv("thresholds/raw_data_merged9.csv")



    # data = pd.concat([data4])

    biases = list(set(data['bias']))
    biases.sort()
    print(biases)

    pf = {'d': [], 'error_probability': [], 'logical_error_rate': [], 'logical_error_rate_eb': [], 'bias': [], 'n_run': []}

    thresholds = []

    for bias in biases:

        plt.figure()

        runs = 0
        data_points = 0

        filtered_data = filter(data, {"bias": bias})
        distances = list(set(filtered_data['d']))
        distances.sort()
        print(bias, distances)
        
        curve_fit_x_data=[]
        curve_fit_y_data=[]
        curve_fit_y_error_data=[]
        colour_wheel=[]
        minmax_er = []
        for c in colours: colour_wheel.append(c)

        # distances = [27,31,35]
        for d in distances:
            filtered_data = filter(data, {"bias":bias, "d": d})
            # print(filtered_data)
            # exit()
            error_probs = list(set(filtered_data['error_probability']))
            error_probs.sort()
            lers=[]
            lers_eb=[]
            # print(bias,d,error_probs)

            minmax_er.append([min(error_probs),max(error_probs)])

            for er in error_probs:
                data_points+=1
                df = filter(data, {'bias':bias,'d':d,"error_probability": er})

                n_run = df['n_run'].sum()

                runs += n_run

                # print(df[['error_probability','bias','d']])

                n_success = df['n_success'].sum()
                pL = 1 - n_success/n_run
                pL_eb = np.sqrt(pL*(1-pL)/n_run)
                print(pL, pL_eb, n_run)
                lers.append(pL)
                lers_eb.append(pL_eb)

                curve_fit_x_data.append([er,d])
                curve_fit_y_data.append(pL)
                curve_fit_y_error_data.append(pL_eb)

                pf['d'].append(d)
                pf['error_probability'].append(er)
                pf['logical_error_rate'].append(pL)
                pf['logical_error_rate_eb'].append(pL_eb)
                pf['bias'].append(bias)
                pf['n_run'].append(n_run)
                # plot_frame.append(pf,ignore_index=True)





            # print(bias, d)
            # print(error_probs)
            # print(lers)
            try: 
                plt.errorbar(error_probs,lers,yerr=np.array(lers_eb), fmt=".", label=f"d={d}",color=colour_wheel.pop())
            except:
                continue

        colour_wheel=[]
        for c in colours: colour_wheel.append(c)
        popt, pcov = curve_fit(threshold_fit, np.array(curve_fit_x_data).T, curve_fit_y_data, sigma=curve_fit_y_error_data,maxfev=5000)
        thresholds.append(popt[-1])

       
        for i, d in enumerate(distances):
            p_min = minmax_er[i][0]
            p_max = minmax_er[i][1]
            x_fit = np.arange(start=p_min,stop=p_max+0.001, step=0.001)

            y_fit=[]
            for val in x_fit:
                y_fit.append(threshold_fit(np.array([val, d]), *popt))

            try:
                plt.plot(x_fit,y_fit,"-",color=colour_wheel.pop())
            except:
                continue





        plt.yscale("log")
        plt.title(f"{CODE_NAME}, bias = {bias}\nruns = {int(runs/data_points)}\nThreshold = {popt[-1]*100:.2f}+-{np.sqrt(np.diag(pcov)[-1])*100:.2f}%")
        plt.xlabel("Physical error rate, p")
        plt.ylabel("Logical error rate, p_L")
        plt.legend()
        plt.yscale('log')
        plt.tight_layout()
        plt.show()
        plt.savefig(f"bias_({bias})_threshold_plot.png")

    