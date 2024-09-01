import glob, os
import json
import numpy as np
import re
import pandas as pd
from scipy.interpolate import interp1d
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.optimize import curve_fit


def filter(data, filter_dict):
    df = data.copy()

    for key, value in filter_dict.items():
        mask = df[key] == value
        df = df[mask]

    return df


colours = ["red", "blue", "green", "red", "purple", "black", "orange"]

if __name__ == "__main__":

    data1 = pd.read_csv("XXXZZZ.csv")
    data2 = pd.read_csv("XZZX.csv")

    # data2 = pd.read_csv("thresholds/raw_data_merged2.csv")
    # data4 = pd.read_csv("thresholds/raw_data_merged4.csv")

    pf = pd.concat([data1, data2])

    #### Sub threshold scaling

    biases = list(set(pf['bias']))
    codes = list(set(pf['code']))
    print(codes)

    for i, bias in enumerate(biases):

        plt.figure()

        for j, code in enumerate(codes):

            df = filter(pf, {'bias': bias})
            df = filter(df, {'code': code})

            # print(df)

            error_probs = list(set(df['error_probability']))

            error_probs.sort()

            for er in error_probs:
                plot_data = filter(df, {"bias": bias, "error_probability": er})

                print(plot_data)

                plt.errorbar(plot_data['d'], plot_data['logical_error_rate'], yerr=plot_data['logical_error_rate_eb'],
                             fmt=".", label=f"{code}, p = {er:.3f}", color=colours[j])

        plt.legend()
        #plt.title(f"bias = {bias}, Sub-threshold scaling: XZZX vs. XXXZZZ")
        plt.xlabel("Code distance, $d$")
        plt.ylabel("Logical error rate, $p_{\mathrm{L}}$")
        plt.yscale('log')
        plt.tight_layout()
        #plt.savefig(f"sub_threshold_bias_({bias}).png")
        #plt.show()



bias = 50.0
plt.figure()
curve_xzzx = filter(pf, {'bias': bias, 'code': 'XZZX', 'error_probability': 0.25})
curve_x3z3 = filter(pf, {'bias': bias, 'code': 'XXXZZZ', 'error_probability': 0.25})
sqrt_n_qubits_x3z3 = np.sqrt(3/4 * (curve_x3z3['d']) ** 2)
sqrt_n_qubits_xzzx = curve_xzzx['d']
sqrt_n_qubits_x3z3_axis = np.linspace(sqrt_n_qubits_x3z3[0], sqrt_n_qubits_x3z3[15], num=100, endpoint=True)
sqrt_n_qubits_xzzx_axis = np.linspace(sqrt_n_qubits_xzzx[0], sqrt_n_qubits_xzzx[4], num=100, endpoint=True)
f_x3z3 = interp1d(sqrt_n_qubits_x3z3, curve_x3z3['logical_error_rate'], kind='linear')
f_xzzx = interp1d(sqrt_n_qubits_xzzx, curve_xzzx['logical_error_rate'], kind='quadratic')
x3z3_fit_param = np.polyfit(sqrt_n_qubits_x3z3, np.log(curve_x3z3['logical_error_rate']), 1)
x3z3_fit = x3z3_fit_param[0] * sqrt_n_qubits_x3z3_axis + x3z3_fit_param[1]
xzzx_fit_param = np.polyfit(sqrt_n_qubits_xzzx, np.log(curve_xzzx['logical_error_rate']), 1)
xzzx_fit = xzzx_fit_param[0] * sqrt_n_qubits_xzzx_axis + xzzx_fit_param[1]

fig, ax = plt.subplots(figsize=(16, 9))
plt.errorbar(sqrt_n_qubits_x3z3, curve_x3z3['logical_error_rate'], yerr=curve_x3z3['logical_error_rate_eb'],
                             fmt="o", label="X$^3$Z$^3$", color='blue', linewidth=5, markersize=20)
plt.plot(sqrt_n_qubits_x3z3_axis, np.exp(x3z3_fit), '-', color='blue', linewidth=5)
plt.errorbar(sqrt_n_qubits_xzzx, curve_xzzx['logical_error_rate'], yerr=curve_xzzx['logical_error_rate_eb'],
                             fmt="s", label="XZZX", color='red', linewidth=5, markersize=20)
plt.plot(sqrt_n_qubits_xzzx_axis, np.exp(xzzx_fit), '-', color='red', linewidth=5)
ax.spines['left'].set_linewidth(3)
ax.spines['right'].set_linewidth(3)
ax.spines['top'].set_linewidth(3)
ax.spines['bottom'].set_linewidth(3)
plt.title(f"Bias $\eta$ = {bias}", size=28)
plt.legend(loc='upper right', prop={'size': 28})
ax.set_yscale('log')
plt.xticks(fontsize=28)
plt.yticks(fontsize=28)
plt.xlabel("$\sqrt{\mathrm{Number \; of \; qubits}}$", size=28)
plt.ylabel("Logical error rate, $p_{\mathrm{L}}$", size=28)
ax.tick_params(axis='both', which='major', direction='out', length=15, width=3, colors='black', grid_color='black', grid_alpha=1)
ax.tick_params(axis='both', which='minor', direction='out', length=7, width=3, colors='black', grid_color='black', grid_alpha=1)
plt.show()
fig.savefig('./Fig_SI_code_subthr-n-qubits-a.pdf', format='pdf', bbox_inches='tight')



bias = 100.0
plt.figure()
curve_xzzx = filter(pf, {'bias': bias, 'code': 'XZZX', 'error_probability': 0.25})
curve_x3z3 = filter(pf, {'bias': bias, 'code': 'XXXZZZ', 'error_probability': 0.25})
sqrt_n_qubits_x3z3 = np.sqrt(3/4 * (curve_x3z3['d']) ** 2)
sqrt_n_qubits_xzzx = curve_xzzx['d']
sqrt_n_qubits_x3z3_axis = np.linspace(sqrt_n_qubits_x3z3[5], sqrt_n_qubits_x3z3[9], num=100, endpoint=True)
sqrt_n_qubits_xzzx_axis = np.linspace(sqrt_n_qubits_xzzx[5], sqrt_n_qubits_xzzx[9], num=100, endpoint=True)
f_x3z3 = interp1d(sqrt_n_qubits_x3z3, curve_x3z3['logical_error_rate'], kind='linear')
f_xzzx = interp1d(sqrt_n_qubits_xzzx, curve_xzzx['logical_error_rate'], kind='quadratic')
x3z3_fit_param = np.polyfit(sqrt_n_qubits_x3z3, np.log(curve_x3z3['logical_error_rate']), 1)
x3z3_fit = x3z3_fit_param[0] * sqrt_n_qubits_x3z3_axis + x3z3_fit_param[1]
xzzx_fit_param = np.polyfit(sqrt_n_qubits_xzzx, np.log(curve_xzzx['logical_error_rate']), 1)
xzzx_fit = xzzx_fit_param[0] * sqrt_n_qubits_xzzx_axis + xzzx_fit_param[1]

fig, ax = plt.subplots(figsize=(16, 9))
plt.errorbar(sqrt_n_qubits_x3z3, curve_x3z3['logical_error_rate'], yerr=curve_x3z3['logical_error_rate_eb'],
                             fmt="o", label="X$^3$Z$^3$", color='blue', linewidth=5, markersize=20)
plt.plot(sqrt_n_qubits_x3z3_axis, np.exp(x3z3_fit), '-', color='blue', linewidth=5)
plt.errorbar(sqrt_n_qubits_xzzx, curve_xzzx['logical_error_rate'], yerr=curve_xzzx['logical_error_rate_eb'],
                             fmt="s", label="XZZX", color='red', linewidth=5, markersize=20)
plt.plot(sqrt_n_qubits_xzzx_axis, np.exp(xzzx_fit), '-', color='red', linewidth=5)
ax.spines['left'].set_linewidth(3)
ax.spines['right'].set_linewidth(3)
ax.spines['top'].set_linewidth(3)
ax.spines['bottom'].set_linewidth(3)
plt.title(f"Bias $\eta$ = {bias}", size=28)
plt.legend(loc='upper right', prop={'size': 28})
ax.set_yscale('log')
plt.xticks(fontsize=28)
plt.yticks(fontsize=28)
plt.xlabel("$\sqrt{\mathrm{Number \; of \; qubits}}$", size=28)
plt.ylabel("Logical error rate, $p_{\mathrm{L}}$", size=28)
ax.tick_params(axis='both', which='major', direction='out', length=15, width=3, colors='black', grid_color='black', grid_alpha=1)
ax.tick_params(axis='both', which='minor', direction='out', length=7, width=3, colors='black', grid_color='black', grid_alpha=1)
plt.show()
fig.savefig('./Fig_SI_code_subthr-n-qubits-b.pdf', format='pdf', bbox_inches='tight')




bias = 100.0
plt.figure()
curve_xzzx = filter(pf, {'bias': bias, 'code': 'XZZX', 'error_probability': 0.25})
curve_x3z3 = filter(pf, {'bias': bias, 'code': 'XXXZZZ', 'error_probability': 0.25})
sqrt_n_qubits_x3z3 = np.sqrt(3/4 * (curve_x3z3['d']) ** 2)
sqrt_n_qubits_xzzx = curve_xzzx['d']
sqrt_n_qubits_x3z3_axis = np.linspace(sqrt_n_qubits_x3z3[5], sqrt_n_qubits_x3z3[9], num=100, endpoint=True)
sqrt_n_qubits_xzzx_axis = np.linspace(sqrt_n_qubits_xzzx[5], sqrt_n_qubits_xzzx[9], num=100, endpoint=True)
f_x3z3 = interp1d(sqrt_n_qubits_x3z3, curve_x3z3['logical_error_rate'], kind='linear')
f_xzzx = interp1d(sqrt_n_qubits_xzzx, curve_xzzx['logical_error_rate'], kind='quadratic')
x3z3_fit_param = np.polyfit(sqrt_n_qubits_x3z3, np.log(curve_x3z3['logical_error_rate']), 1)
x3z3_fit = x3z3_fit_param[0] * sqrt_n_qubits_x3z3_axis + x3z3_fit_param[1]
xzzx_fit_param = np.polyfit(sqrt_n_qubits_xzzx, np.log(curve_xzzx['logical_error_rate']), 1)
xzzx_fit = xzzx_fit_param[0] * sqrt_n_qubits_xzzx_axis + xzzx_fit_param[1]

fig, ax = plt.subplots(figsize=(16, 9))
plt.errorbar(sqrt_n_qubits_x3z3, curve_x3z3['logical_error_rate'], yerr=curve_x3z3['logical_error_rate_eb'],
                             fmt="o", label="X$^3$Z$^3$ DW code", color='blue', linewidth=5, markersize=20)
plt.plot(sqrt_n_qubits_x3z3_axis, np.exp(x3z3_fit), '-', color='blue', linewidth=5)
plt.errorbar(sqrt_n_qubits_xzzx, curve_xzzx['logical_error_rate'], yerr=curve_xzzx['logical_error_rate_eb'],
                             fmt="s", label="XZZX code", color='red', linewidth=5, markersize=20)
plt.plot(sqrt_n_qubits_xzzx_axis, np.exp(xzzx_fit), '-', color='red', linewidth=5)
ax.spines['left'].set_linewidth(3)
ax.spines['right'].set_linewidth(3)
ax.spines['top'].set_linewidth(3)
ax.spines['bottom'].set_linewidth(3)
#plt.title(f"Bias $\eta$ = {bias}", size=28)
plt.legend(loc='upper right', prop={'size': 28})
ax.set_yscale('log')
plt.xticks(fontsize=28)
plt.yticks(fontsize=28)
plt.xlabel("$\sqrt{\mathrm{Number \; of \; qubits}}$", size=28)
plt.ylabel("Logical error rate, $p_{\mathrm{L}}$", size=28)
ax.tick_params(axis='both', which='major', direction='out', length=15, width=3, colors='black', grid_color='black', grid_alpha=1)
ax.tick_params(axis='both', which='minor', direction='out', length=7, width=3, colors='black', grid_color='black', grid_alpha=1)
plt.show()
fig.savefig('./Fig_2_b.pdf', format='pdf', bbox_inches='tight')

