from pdsketch import Diagram
from multimatching import dB

A = Diagram([(2,3), (5,10)])
B = Diagram([(5,11), (9,10)])

dB(A, B)
