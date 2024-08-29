import numpy as np
from qecsim import paulitools as pt
# import the error model
from qecsim.models.generic import BiasedDepolarizingErrorModel
# import the code
from models.XXXZZZ import Color666CodeXXXZZZ
# import the decoder
from models.XXXZZZ import Color666MPSDecoder

# initialise models
my_code = Color666CodeXXXZZZ(5)
my_error_model = BiasedDepolarizingErrorModel(bias=3, axis='Z')
my_decoder = Color666MPSDecoder(chi=12)

# print models
print(my_code)
print(my_error_model)
print(my_decoder)

# set physical error probability to 10%
error_probability = 1.0

# seed random number generator for repeatability
# rng = None # np.random.default_rng(13)
rng = np.random.default_rng(10)

# error: random error based on error probability
error = my_error_model.generate(my_code, error_probability, rng)

# syndrome: stabilizers that do not commute with the error
syndrome = pt.bsp(error, my_code.stabilizers.T)

# recovery: best match recovery operation based on decoder
recovery = my_decoder.decode(my_code, syndrome, error_model=my_error_model)


# check recovery ^ error commutes with stabilizers (by construction)
print("error-stabilizers commutator")
print(pt.bsp(recovery ^ error, my_code.stabilizers.T))

# success iff recovery ^ error commutes with logicals
print(pt.bsp(recovery ^ error, my_code.logicals.T))

print(my_code.new_pauli(error))

"""
# print(my_code.new_pauli(error))
print("max recovery:")
print(my_code.new_pauli(recovery))

print("any recovery:")
any_recovery = my_decoder.sample_recovery(my_code, syndrome)
print(any_recovery)

print("syndrome:")
print(syndrome)

# print logical X
print('logical X:')
print(my_code.new_pauli().logical_x())

# print logical Z
print('logical Z:')
print(my_code.new_pauli().logical_z())

# print a dual plaquette
print('Example of an X plaquette:')
print(my_code.new_pauli().plaquette('X', [3, 2]))


# check recovery ^ error commutes with stabilizers (by construction)
print("error-stabilizers commutator")
print(pt.bsp(recovery ^ error, my_code.stabilizers.T))
"""
