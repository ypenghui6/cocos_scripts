import numpy as np
import matplotlib.pyplot as plt
 
x=np.linspace(1, 50000000, 1000000)
y=40000000 * ( (1+ x/60000000)**0.4-1)
plt.figure()
plt.plot(x,y)
plt.savefig("test2.jpg")
