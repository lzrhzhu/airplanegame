import matplotlib.pyplot as plt
plane_x = [1, 1.5, 2, 2.5, 3, 3, 4, 4, 3.5, 3, 2.5, 2, 1.5, 1.5, 1]
plane_y = [1, 2, 2.5, 3, 2.5, 2, 2, 1, 1, 0.5, 0, 0.5, 1, 0.5, 1]
plt.plot(plane_x, plane_y, "b")
plt.fill(plane_x, plane_y, "b")
plt.show()