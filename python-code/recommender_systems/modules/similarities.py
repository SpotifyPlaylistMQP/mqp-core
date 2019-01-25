from math import *

def cosine(vector1, vector2):
    numerator = sum(a * b for a, b in zip(vector1, vector2))
    denominator = sqrt(sum(a * a for a in vector1)) * sqrt(sum(b * b for b in vector2))
    if denominator == 0:
        return 0
    return round(numerator / denominator, 5)

def jaccard(col1, col2):
    numerator = 0
    denominator = 0

    for a, b in zip(col1, col2):
        if (a == b) and (a == 1) and (b == 1):
            numerator += 1
            denominator += 1
        elif (a == 1) and (b == 0):
            denominator += 1
        elif (a == 0) and (b == 1):
            denominator += 1

    return numerator / denominator