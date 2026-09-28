from core import *

filename = 'intro/FileC056.txt'
with open(filename, 'r') as file:
    data_str = file.read()
data = [a.split() for a in data_str.split('\n')[7:-1]]
time_s = np.array([float(a[3]) for a in data]) * 1e-3
sipm = np.array([float(a[6]) for a in data])
deadtime_s = np.array([float(a[9]) for a in data]) * 1e-6
coincidence = np.array([int(a[10])==1 for a in data])
bin_time = 100
bins = 500  
total_time = bin_time * bins
skip = 1
interval_counts,_ = np.histogram(time_s, skip*bins, range=(time_s[0], time_s[0] + skip*total_time))
interval_counts = interval_counts[skip*np.int64(np.arange(bins))]
plt_range = np.arange(150, 240)
mean = np.mean(interval_counts)
count_hist = np.bincount(interval_counts)
count_hist_err = np.sqrt(count_hist)
count_arr = np.arange(len(count_hist))
poisson = scipy.stats.poisson.pmf(count_arr, mean) * bins
plt.bar(count_arr[plt_range], count_hist[plt_range], yerr = count_hist_err[plt_range], width=1)
plt.plot(count_arr[plt_range], poisson[plt_range], color='orange')
plt.xlabel('Number of counts in interval')
plt.ylabel('Occurrences')
plt.title('Distribution of counts per interval, Poisson fit')
plt.figure()
#only use nonzero values to calculate chi square
nonzero = count_hist != 0
X2_poisson = np.sum(((count_hist - poisson)**2 / poisson)[nonzero])
print(f'Poisson X2 {X2_poisson} / {np.sum(nonzero) - 1} dof')
def poisson_gaussian(mu, x):
    return scipy.stats.norm.pdf(x, mu, np.sqrt(mu)) * bins
def gaussian_X2(mu):
    gaussian_counts = poisson_gaussian(mu, count_arr)
    return np.sum(((count_hist - gaussian_counts)**2 / gaussian_counts)[nonzero])
res = scipy.optimize.minimize(gaussian_X2, mean)
print(f'Gaussian X2 {res.fun} / {np.sum(nonzero) - 1} dof')
plt.bar(count_arr[plt_range], count_hist[plt_range], yerr = count_hist_err[plt_range], width=1)
plt.plot(count_arr[plt_range], poisson_gaussian(res.x, count_arr)[plt_range], color='red')
plt.xlabel('Number of counts in interval')
plt.ylabel('Occurrences')
plt.title('Distribution of counts per interval, Gaussian fit')
"""
plt.bar(np.arange(bins), count_hist, width=1)
plt.xlabel('Interval')
plt.ylabel('Counts')
plt.title('Counts per 10 second interval')
plt.figure()
running_avg = np.array([np.mean(count_hist[:i+1]) for i in range(bins)])
std = np.std(count_hist)
errbar = std / np.sqrt(np.arange(bins) + 1)
plt.errorbar(np.arange(bins), running_avg, yerr = errbar, fmt='ro', linestyle='None')
plt.xlabel('Number of intervals')
plt.ylabel('Running average')
plt.title('Running average of counts per interval')
mean1 = np.mean(count_hist)
err1 = std / np.sqrt(bins)
count_hist_2,_ = np.histogram(time_s, bins, range = (time_s[0] + total_time, time_s[0] + 2*total_time))
mean2 = np.mean(count_hist_2)
err2 = np.std(count_hist_2) / np.sqrt(bins)
print(f'Mean 1: {mean1} +- {err1}')
print(f'Mean 2: {mean2} +- {err2}')
"""
"""
plt.hist(sipm, bins=200)
plt.xlabel('Amplitude (mV)')
plt.ylabel('Count')    
plt.title('All events')
plt.figure()
plt.hist(sipm[coincidence], bins=200)
plt.xlabel('Amplitude (mV)')
plt.ylabel('Count')    
plt.title('Coincidence events')
plt.figure()
time_intervals = (time_ms[1:] - time_ms[:-1]) * 1e-3
corrected_intervals = time_intervals - deadtime_us[:-1] * 1e-6
print(f'Raw rate {1/np.mean(time_intervals)}')
print(f'Corrected rate {1/np.mean(corrected_intervals)}')
plt.hist(time_intervals, bins=200)
plt.xlabel('Raw time interval (s)')
plt.ylabel('Count')
plt.title('Raw interval frequency')
plt.hist(corrected_intervals, bins=200)
plt.xlabel('Corrected time interval (s)')
plt.ylabel('Count')
plt.title('Corrected interval frequency')
"""
plt.show()