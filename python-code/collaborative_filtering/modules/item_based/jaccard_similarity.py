def calculate(col1, col2):
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