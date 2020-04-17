import numpy as np
import matplotlib.pyplot as plt
 
x=np.linspace(1, 5000, 100)
y=2000 * ( (1+ x/8000)**0.4-1)
plt.figure()
plt.plot(x,y)
plt.savefig("test4.jpg")
