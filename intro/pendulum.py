from core import *

T = 1000
filename = 'pendulum_long.npz'

min_brightness = 10
def avg_x(img):
    cv2.imshow('raw', img)
    cv2.waitKey(1)
    mask = np.mean(img, axis=2) < min_brightness
    cv2.imshow('proc', np.uint8(mask) * 255)
    cv2.waitKey(1)
    return np.sum(np.arange(img.shape[1]) * mask) / np.sum(mask)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_EXPOSURE, -6)
input(f'Measure')
t = []
x = []
start = time()
while time() - start < T:
    _,img = cap.read()
    t.append(time())
    x.append(avg_x(img))
np.savez(filename, **{'t':np.array(t),'x':np.array(x)})