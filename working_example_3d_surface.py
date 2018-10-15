
from mpl_toolkits.mplot3d import axes3d, Axes3D #<-- Note the capitalization! #INSTEAD OF from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

fig = plt.figure()

ax = Axes3D(fig) #<-- Note the difference from your original code... #INSTEAD OF ax = fig.gca(projection='3d')

X, Y, Z = axes3d.get_test_data(0.05)
cset = ax.contour(X, Y, Z, 16, extend3d=True)
ax.clabel(cset, fontsize=9, inline=1)
plt.show()



