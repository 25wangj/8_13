from core import *

def period(filename):
    data = np.load(filename)
    start = 10
    t = data['t'][start:]
    t = t - t[0]
    x = data['x'][start:]
    frame = t[-1] / len(t)
    x0 = np.mean(x)
    cross = (x[:-1] < x0) & (x[1:] >= x0)
    n_cross = np.sum(cross)
    t_cross = t[:-1][cross]
    period_coarse = (t_cross[-1] - t_cross[0]) / (n_cross - 1)
    win = int(period_coarse / frame)
    x_sum = np.cumsum(x)
    x_avg = (x_sum[win:] - x_sum[:-win]) / win
    x_sub = x[win:] - x_avg
    #plt.plot(t[win:], x_sub)
    #plt.show()     
    return ufloat(t_cross[-1] - t_cross[0], 0) / (n_cross - 1)

T_short = period('intro/pendulum_short.npz')
T_long = period('intro/pendulum_long.npz')
M = 7.4e-3 * ufloat(1, 0.1)
lam = ufloat(2.7e-5, 1e-6)
L = ufloat(0.51, 5e-3)
I = 2.8e-7 * ufloat(1, 0.1)
d_short = 0.20981
d_long = 0.01867
d = ufloat(d_short - d_long, 5e-5)
k = d/L
a = I/(M*L**2)
b = lam*L/M
g = 4*np.pi**2 * d / ((1 - 1/(1+k)**2 * a + (1+k)/6*b)*T_long**2 - (1-a+1/6*b)*T_short**2)
print(g)