from core import *

def get_T2(i, tau,  min_v, n_pulse, pulse_range):
    with open(f'ex1_nmr/glycerin_data/TEK{i:04d}.CSV', 'r') as file:
        data_str = file.read()
    data = [a.split(',') for a in data_str.split('\n')[18:-1]]
    t = np.array([float(a[3]) for a in data])
    v = np.array([float(a[4]) for a in data])
    #plt.plot(t,v)

    t_start = t[np.flatnonzero(np.abs(v - np.mean(v)) > min_v)[0]]
    t_pulse = []
    v_pulse = []
    #plt.figure()
    for i in range(n_pulse):
        t_min = t_start + (2*pulse_range[0] + 2*i + 1)*tau
        t_max = t_start + (2*pulse_range[1] + 2*i + 1)*tau
        inds = (t > t_min) & (t < t_max)
        t_pulse.append(t_start + 2*(i+1)*tau)
        v_pulse.append(np.std(v[inds]))
        #plt.plot(t[inds], v[inds])
    #plt.figure()
    #plt.scatter(t_pulse, np.log(v_pulse))
    popt,pcov = fit(lambda x,a,b: a*x+b, t_pulse, np.log(v_pulse))
    #print(-1/popt[0])
    return -1/popt[0]

#Formula for log of viscosity of glycerol water-mixture, in Pa*s
#Function fitted to https://web.cecs.pdx.edu/~gerry/class/EAS361/lab/pdf/glycerinWaterViscosity_Dorsey.pdf
def log_viscosity(f):
    return -5.00879 + 5.35636 * f**4.02136

tau = 2e-3
min_v = 0.01
n_pulse = 4
pulse_range = [0.2, 0.8]

with open('ex1_nmr/glycerin_manifest_1.txt', 'r') as file:
    data_str = file.read()
data = [a.split() for a in data_str.split('\n')[1:-1]]
f_arr = []
t2_arr = []
for a in data:
    f = ufloat(float(a[0]), float(a[1])) * 0.01
    f_arr.append(f)
    t2_curr = []
    for i in range(int(a[2]), int(a[3])+1):
        t2_curr.append(get_T2(i, tau, min_v, n_pulse, pulse_range))
    t2_arr.append(ufloat(np.mean(t2_curr), np.std(t2_curr) / np.sqrt(len(t2_curr))))
plt.figure()
plt.errorbar(vals(f_arr), vals(t2_arr), xerr=errs(f_arr), yerr=errs(t2_arr), fmt='o')
plt.title('T2 vs glycerin concentration')
log_visc_arr = log_viscosity(np.asarray(f_arr))
log_t2_arr = unumpy.log(t2_arr)
popt, pcov = fit(lambda x,a,b:a*x+b, vals(log_visc_arr), vals(log_t2_arr), sigma=errs(log_t2_arr))
fig = plt.figure()
plt.errorbar(vals(log_visc_arr), vals(log_t2_arr), xerr=errs(log_visc_arr), yerr=errs(log_t2_arr), fmt='o')
plt.plot(vals(log_visc_arr), popt[0] * vals(log_visc_arr) + popt[1])
plt.title('Log T2 vs log viscosity')
plt.xlabel(r'$\ln(\eta/(\text{Pa}\cdot\text{s}))$')
plt.ylabel(r'$\ln(T_2/\text{s})$')
plt.text(.95, .95, f'slope = {popt[0]:.3f} $\pm$ {np.sqrt(pcov[0,0]):.3f}', ha='right', va='top', transform=fig.get_axes()[0].transAxes)

plt.show()