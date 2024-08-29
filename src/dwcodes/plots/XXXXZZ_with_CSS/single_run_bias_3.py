import numpy as np
from qecsim import paulitools as pt

# import the error model
from models.XXXXZZ_with_CSS import BiasedDepolarizingErrorModel
# import the code
from models.XXXXZZ_with_CSS import Color666CodeXXXXZZ
# import the decoder
from models.XXXXZZ_with_CSS import Color666MPSDecoderXXXXZZSimulated

# initialise models
my_code = Color666CodeXXXXZZ(9)
my_error_model = BiasedDepolarizingErrorModel(bias=3, axis='Z')
my_decoder = Color666MPSDecoderXXXXZZSimulated(chi=20)

# print models
print(my_code)
print(my_error_model)
print(my_decoder)

# set physical error probability to 10%
error_probability = 1.0

# seed random number generator for repeatability
rng = np.random.default_rng()

# error: random error based on error probability
error = my_error_model.generate(my_code, error_probability, rng)

# syndrome: stabilizers that do not commute with the error
syndrome = pt.bsp(error, my_code.stabilizers.T)

# recovery: best match recovery operation based on decoder
recovery = my_decoder.decode(my_code, syndrome, error_model=my_error_model)

# check recovery ^ error commutes with stabilizers (by construction)
print(pt.bsp(recovery ^ error, my_code.stabilizers.T))

# success iff recovery ^ error commutes with logicals
print(pt.bsp(recovery ^ error, my_code.logicals.T))

print(my_code.new_pauli(error))
