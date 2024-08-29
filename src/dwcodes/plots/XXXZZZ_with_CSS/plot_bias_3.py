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
codes = [Color666CodeXXXZZZ(size) for size in [3, 5, 7]]
error_model = BiasedDepolarizingErrorModel(bias=3, axis='Z')
decoder = Color666MPSDecoderXXXZZZSimulated(chi=20)

# print models
print(codes)
print(error_model)
print(decoder)

# set physical error probabilities
error_probability_min, error_probability_max = 0.05, 0.5
error_probabilities = np.linspace(error_probability_min, error_probability_max, 10)

# set max_runs for each probability
max_runs = 1000

# print run parameters
print('Codes:', [code.label for code in codes])
print('Error model:', error_model.label)
print('Decoder:', decoder.label)
print('Error probabilities:', error_probabilities)
print('Maximum runs:', max_runs)

# run simulations and print data from middle run to view format
data = [app.run(code, error_model, decoder, error_probability, max_runs=max_runs)
        for code in codes for error_probability in error_probabilities]
print(data[len(data)//2])

# prepare code to x,y map and print
code_to_xys = {}
for run in data:
    xys = code_to_xys.setdefault(run['code'], [])
    xys.append((run['physical_error_rate'], run['logical_failure_rate']))
print('\n'.join('{}: {}'.format(k, v) for k, v in code_to_xys.items()))

# format plot
fig = plt.figure(1, figsize=(12, 9))
plt.title('X3Z3 simulated with CSS \n({} error model, {} decoder)'.format(error_model.label, decoder.label))
plt.xlabel('Physical error rate')
plt.ylabel('Logical failure rate')
plt.xlim(error_probability_min-0.05, error_probability_max+0.05)
# plt.ylim(-0.05, 0.85)

# add data
for code, xys in code_to_xys.items():
    plt.plot(*zip(*xys), 'x-', label='{} code'.format(code))
plt.legend(loc='lower right')
#plt.yscale('log')
plt.grid()
plt.xticks(np.arange(error_probability_min, error_probability_max, 0.02))
plt.show()
