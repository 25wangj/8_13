from core import *

init_time = 1e-4
eps = 1.15e-3
min_v = 0.005
pulse_range = [0.2, 0.8]
def get_pulse(i,tau):
    with open(f'ex1_nmr/paramagnetic_data/TEK{i:04d}.csv', 'r') as file:
        data_str = file.read()
    data = [a.split(',') for a in data_str.split('\n')[18:-1]]
    t = np.array([float(a[3]) for a in data])
    v = np.array([float(a[4]) for a in data])
    v0 = np.mean(v[t - t[0] < init_time])
    t_start = t[np.abs(v - v0) > min_v][0]
    t_min = t_start + eps * (1 + 2 * pulse_range[0])
    t_max = t_start + eps * (1 + 2 * pulse_range[1])
    mask = (t > t_min) & (t < t_max)
    #plt.plot(t[mask] - t_start + tau, v[mask])
    return np.std(v[mask])

tau_arr = []
i_arr = []
concs = []
N = 0
with open('ex1_nmr/paramagnetic_manifest.txt', 'r') as file:
    data_str = file.read()
data = [a.split() for a in data_str.split('\n')[1:]]
i = 0
while i < len(data):
    start = True
    N += 1
    concs.append(float(data[i][0]))
    tau_curr = []
    i_curr = []
    while i < len(data) and (start or len(data[i]) == 2):
        start = False
        tau_curr.append(float(data[i][-1]) * 1e-3)
        i_curr.append(int(data[i][-2]))
        i += 1
    tau_arr.append(tau_curr)
    i_arr.append(i_curr)

t1s = []
t1_errs = []
for j in range(N):
    v_arr = []
    #plt.figure()
    for (i,tau) in zip(i_arr[j], tau_arr[j]):
        v_arr.append(get_pulse(i,tau))
    #plt.figure()
    def shifted_exp(t,t2,v0):
        return v0 * (2*np.exp(-t/t2) - 1)
    v0_est = v_arr[0]
    T1_est = -2 * v0_est / ((v_arr[1] - v_arr[0]) / (tau_arr[j][1] - tau_arr[j][0]))
    popt, pcov = fit(shifted_exp, tau_arr[j], v_arr, p0=[T1_est, v0_est])
    t1s.append(ufloat(popt[0], np.sqrt(pcov[0,0])))
plt.errorbar(np.log(concs), vals(unumpy.log(t1s)), yerr=errs(unumpy.log(t1s)))
plt.xlabel(r'$\ln[\text{Fe}^{3+}]$')
plt.ylabel('$\ln(T_1)$')
plt.title('$T_1$ vs ion concentration')
plt.show()