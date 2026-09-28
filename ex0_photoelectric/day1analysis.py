from core import *

c = 2.998e8
q_e = 1.602e-19

with open('ex0_photoelectric/day1data.txt', 'r') as file:
    data_str = file.read()
data = [[float(f) for f in a.split()] for a in data_str.split('\n')[1:]]
Lambda = []
V = []
I = []
i = 0
n = 0
#Only use data near cutoff
min_V = [3, 4, 3, 3.5, 3.5]
while i < len(data):
    Lambda.append(data[i][0] * 1e-9)
    curr_V = [data[i][1]]
    curr_I = [data[i][2] * 1e-12]
    i += 1
    while i < len(data) and len(data[i]) == 2:
        curr_V.append(data[i][0])
        curr_I.append(data[i][1] * 1e-12)
        i += 1
    curr_V = np.array(curr_V)   
    curr_I = np.array(curr_I)
    sort_inds = np.argsort(curr_V)
    curr_V = curr_V[sort_inds]
    curr_I = curr_I[sort_inds]
    mask = curr_V >= min_V[n]
    V.append(curr_V[mask])
    I.append(curr_I[mask])
    n += 1
Lambda = np.array(Lambda)
Omega = 2*np.pi*c/Lambda

def softplus(x, x0, y0, m, a):
    return m*a*np.log(1 + np.exp(-(x-x0)/a)) + y0
fun = softplus
p0 = [4,1e-15,2e-14,1]

sigma_I = 1e-16
fig, axs = plt.subplots(2,3)
V0 = []
V0_err = []
for i in range(n):
    sigma = np.full(len(V[i]), sigma_I)
    popt, pcov, info, _, _ = scipy.optimize.curve_fit(fun, V[i], I[i], sigma=sigma, p0 = p0, full_output=True)
    I_fit = fun(V[i], *popt)
    V0.append(popt[0])
    V0_err.append(np.sqrt(pcov[0,0]))

    ax:plt.Axes = axs.flat[i]
    ax.errorbar(V[i], I[i], yerr = sigma, fmt='o')
    ax.plot(V[i], I_fit)
    ax.text(.99, .99, f'V0 = {V0[i]:.3f} $\pm$ {V0_err[i]:.3f}', ha='right', va='top', transform=ax.transAxes)
    ax.set_title(f'{Lambda[i]*1e9:.0f} nm')
    ax.set_xlabel('V')
    ax.set_ylabel('I')
V0 = np.array(V0)
V0_err = np.array(V0_err)
axs.flat[-1].axis('off')
plt.tight_layout()

popt, pcov, info, _, _ = scipy.optimize.curve_fit(lambda x,a,b: a*x+b, Omega, V0, sigma = V0_err, full_output=True)
Omega_range = np.array([np.min(Omega), np.max(Omega)])
print(f'hbar = {popt[0] * q_e : .2E} +- {np.sqrt(pcov[0,0]) * q_e:.2E}')
print(f'phi = {-popt[1] : .2E} +- {np.sqrt(pcov[1,1]) : .2E}')
plt.figure()
plt.errorbar(Omega, V0, yerr= V0_err, fmt='o')
plt.plot(Omega_range, popt[0] * Omega_range + popt[1])
plt.xlabel('$\omega$')
plt.ylabel('V')
plt.tight_layout()
plt.show()