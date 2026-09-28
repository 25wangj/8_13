from core import *

def gaussian(x, mu, sigma): 
    return scipy.stats.norm.pdf(x, mu, sigma) * bin_width * n
def cauchy(x, mu, sigma):
    return scipy.stats.cauchy.pdf(x, mu, sigma) * bin_width * n

with open('intro/pendulumData.csv', 'r') as file:
    data_str = file.read()
data = [a.split(',') for a in data_str.split('\n')[:-1]]
g_arr = np.array([float(a[1]) for a in data[1:]])
#Egregious outliers
g_range = [1,20]
g_arr = g_arr[(g_arr > g_range[0]) & (g_arr < g_range[1])]
n = len(g_arr)
bin_width = 0.05
bins = int((g_range[1] - g_range[0]) / bin_width)
g_hist,_ = np.histogram(g_arr, bins, range = g_range)
g_list = np.linspace(g_range[0], g_range[1], bins)
sigma = np.sqrt(g_hist)
sigma_fit = np.where(sigma == 0, 1e6, sigma)
fun = cauchy
name = 'Cauchy'
popt, pcov, info,_,_ = scipy.optimize.curve_fit(fun, g_list, g_hist, p0=[9.8, 0.2], sigma=sigma_fit, full_output=True)
X2 = np.sum(info['fvec']**2)
dof = np.sum(sigma != 0) - 2
curve = fun(g_list,  *popt)
plt_range = [9,11]
mask = (g_list > plt_range[0]) & (g_list < plt_range[1])
plt.bar(g_list[mask], g_hist[mask], width = bin_width, yerr = sigma[mask])
plt.plot(g_list[mask], curve[mask], color='orange')
print(f'X2 {X2} / {dof} dof')
plt.xlabel('$g$ value (m/s$^2$)')    
plt.ylabel('Counts')
plt.annotate(f'$\\mu$ = {popt[0]:.3f} $\\pm$ {np.sqrt(pcov[0,0]):.3f}', (0.7, 0.9) , xycoords = 'axes fraction')
plt.title(f'JLab pendulum measurements, {name} fit')
plt.show()