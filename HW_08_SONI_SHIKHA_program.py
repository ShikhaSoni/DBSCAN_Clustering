import numpy as num
import sys
from scipy.spatial import distance
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

data = None 
noise = None
four = []
count = []
cluster_list = []
assigned = []
class Cluster():
	def __init__(self):
		self.Points = []
class Main():
	def readFile(self, file):
		data = num.genfromtxt(file, delimiter=",")
		return data
	def DBSCAN(self, eps, Min):
		#find the points in 1.2 euclidean distance
		global noise
		noise = []
		index = 0
		visited = {}
		for i in range(0, num.shape(data)[0]):
			visited[i] = 0
		for point in data:
			if visited[index] == 0:
				visited[index] = 1
				neighbors = self.find_distance(eps, index, visited)
				if len(neighbors) < Min:
					noise.append(index)
				else:
					cluster = Cluster()
					visited = self.expand(eps, Min, index, cluster, neighbors, visited)
			index += 1

	def expand(self, eps, Min, index, cluster, neighbors, visited):	
		cluster.Points.append(data[index])
		assigned.append(index)
		for n in neighbors:
			if visited[n] == 0:
				visited[n] = 1
				other_neighbors = self.find_distance(eps, n, visited)
				#if len(other_neighbors) < Min:
				#	noise.append(n)
				#else:
				neighbors += other_neighbors
			if n not in assigned:
				cluster.Points.append(data[n])
				assigned.append(n)
		cluster_list.append(cluster)
		return visited

	def find_distance(self, eps, point, visited):
		count.append(data[point])
		n = []
		dists = []
		index = 0
		for each in data:
			dists.append(distance.euclidean(data[point], each))
			if(distance.euclidean(each, data[point]) <= eps):
				if visited[index] == 0:
					n.append(index)
			index += 1
		dists.sort()
		four.append(dists[3])
		four.sort()
		return n
		

def main():
	main = Main()
	global data
	data = main.readFile(sys.argv[1])
	main.DBSCAN(float(sys.argv[2]), int(sys.argv[3]))
	sum = 0
	for c in cluster_list:
		sum += len(c.Points)
		print("Cluster Points: ", len(c.Points))
	print("Clusters: ", len(cluster_list))
	print("Noise: ",len(noise))
	cl_data = [len(clust.Points) for clust in cluster_list]
	print("Number of points ", cl_data)
	plt.plot(four)
	plt.xlabel('All Stars')
	plt.ylabel('4th closest start distance')
	plt.show()
	x_list = []
	y_list = []
	z_list = []
	for point in data:
		x_list.append(point[0])
		y_list.append(point[1])
		z_list.append(point[2])

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(x_list, y_list, z_list)
	plt.title('All points in the galaxy')
	plt.show()
	#print(sum + len(noise))
main()
