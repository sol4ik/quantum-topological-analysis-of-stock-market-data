import matplotlib.pyplot as plt

# takens' embedding
data = [32.74, 32.36, 33.15, 32.81, 31.19, 33.57, 33.85]
points_3d = list()
for i in range(len(data) - 2):
    points_3d.append([data[i + j] for j in range(3)])

# visualize
#2d plot
# fig, ax = plt.subplots()
# ax.plot(range(len(data)), data)
# ax.get_xaxis().set_ticklabels([])
# plt.show()

# 3d plot
squished_points = points_3d
for point in squished_points:
    point = list([i / 10 for i in point])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for point in squished_points:
    ax.scatter(point[0], point[1], point[2], marker='o')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

ax.get_xaxis().set_ticklabels([])
ax.get_yaxis().set_ticklabels([])
ax.get_zaxis().set_ticklabels([])

plt.show()
