import numpy as np
import matplotlib.pyplot as plt
from qecsim import app
# import the error model
from models.XXXZZZ_with_CSS import BiasedDepolarizingErrorModel
# import the code
from models.XXXZZZ_with_CSS import Color666CodeXXXZZZ
# import the decoder
from models.XXXZZZ_with_CSS import Color666MPSDecoderXXXZZZSimulated

# set models
codes = [Color666CodeXXXZZZ(size) for size in [3, 5, 7, 9, 11]]
error_model = BiasedDepolarizingErrorModel(bias=3, axis='Z')
decoder = Color666MPSDecoderXXXZZZSimulated(chi=36)

# print models
print(codes)
print(error_model)
print(decoder)

# set physical error probabilities
error_probability = 0.1

# set max_runs for each probability
max_runs = 100

# print run parameters
print('Codes:', [code.label for code in codes])
print('Error model:', error_model.label)
print('Decoder:', decoder.label)
print('Error probability:', error_probability)
print('Maximum runs:', max_runs)

# run simulations and print data from middle run to view format
data = [app.run(code, error_model, decoder, error_probability, max_runs=max_runs)
        for code in codes]

# prepare code to x,y map and print

error_vs_d = list()
error_vs_n = list()
for run in data:
    error_vs_n.append((np.sqrt(run['n_k_d'][0]), run['logical_failure_rate']))


fig, ax = plt.subplots(figsize=(16, 9))
ax.plot(*zip(*error_vs_n), color='red', marker='o', linestyle='dashed',
    linewidth=4, markersize=18, label='XXXZZZ code')
ax.spines['left'].set_linewidth(2)
ax.spines['right'].set_linewidth(2)
ax.spines['top'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
plt.legend(loc='lower left', prop={'size': 26})
plt.xticks(fontsize=34)
plt.yticks(fontsize=34)
#plt.xlabel('Code distance $\it{d}$', size=34)
plt.xlabel('Number of qubits', size=34)
plt.ylabel('Logical failure rate', size=34)
plt.yscale('log')
plt.show()

