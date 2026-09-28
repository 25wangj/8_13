from core import *

def linear_fit(x, y, title, sigma, ax:plt.Axes):
    popt, pcov, info, _, _ = scipy.optimize.curve_fit(lambda x,a,b: a*x+b, x, y, sigma=sigma, full_output=True)
    ax.errorbar(x, y, yerr=sigma, fmt='o')
    ax.plot(x, popt[0] * x + popt[1])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    X2 = np.sum(info['fvec']**2)
    dof = len(x)-2
    P = 1-scipy.stats.chi2.cdf(X2, dof)
    text = f'y = ax+b\n a= {popt[0]:.2f} $\pm$ {np.sqrt(pcov[0,0]):.2f}\nb= {popt[1]:.2f} $\pm$ {np.sqrt(pcov[1,1]):.2f}\n$\chi^2$/dof = {np.sum(info['fvec']**2):.1f}/{len(x)-2}\nP = {P:.3f}'
    ax.text(.01, .99, text, ha='left', va='top', transform=ax.transAxes)
    ax.set_title(title)

sigma = 2.5
with open('intro/anscombe.txt', 'r') as file:
    data_str = file.read()
data = [a.split() for a in data_str.split('\n')]
fig, axs = plt.subplots(2,2)
for i in range(4):
    x = np.array([float(a[2*i]) for a in data])
    y = np.array([float(a[2*i+1]) for a in data])
    sigma_y = np.full(len(y), sigma)
    ax = axs.flat[i]
    linear_fit(x, y, f'Data set {i}', sigma_y, ax)
plt.tight_layout()
plt.show()