import numpy as np
import matplotlib.pyplot as plt
 
x=np.linspace(1, 5000, 100)
y=2000 * ( (1+ 1000/x)**0.4-1)
plt.figure()
plt.plot(x,y)
plt.savefig("test5.jpg")
