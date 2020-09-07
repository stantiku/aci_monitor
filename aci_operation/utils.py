# A simple function to change long numbers to K format
# Code from 
# https://stackoverflow.com/questions/579310/formatting-long-numbers-as-strings-in-python/45846841

def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'G', 'T'][magnitude])

