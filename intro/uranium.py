from core import *

filename = 'intro/uranium.spe'
with open(filename, 'r') as file:
    data_str = file.read()
data = [a for a in data_str.split('\n')[12:-18]]
counts = [float(a) for a in data][:300]

plt.bar(np.arange(len(counts)), counts, width=1)
plt.title('Uranium Spectrum')
plt.xlabel('Bin')
plt.ylabel('Counts')
plt.show()