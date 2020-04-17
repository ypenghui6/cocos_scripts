import numpy as np
import matplotlib.pyplot as plt
 
x=np.linspace(1, 50000000, 1000000)
y=30000000 * ( (1+ x/70000000)**0.4-1)
plt.figure()
plt.plot(x,y)
plt.savefig("test3.jpg")
