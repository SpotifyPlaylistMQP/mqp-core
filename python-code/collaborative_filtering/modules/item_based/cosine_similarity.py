from math import *

def calculate(vector1, vector2):
    numerator = sum(a * b for a, b in zip(vector1, vector2))
    denominator = sqrt(sum(a * a for a in vector1)) * sqrt(sum(b * b for b in vector2))
    return round(numerator / denominator, 5)