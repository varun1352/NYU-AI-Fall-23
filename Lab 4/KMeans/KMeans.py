import argparse
import csv

def euclidean_distance_squared(point1, point2):
    return sum((x - y) ** 2 for x, y in zip(point1, point2))

def manhattan_distance(point1, point2):
    return sum(abs(x - y) for x, y in zip(point1, point2))

def calculate_distance(point1, point2, distance_metric):
    if distance_metric == 'e2':
        return euclidean_distance_squared(point1, point2)
    elif distance_metric == 'manh':
        return manhattan_distance(point1, point2)
    else:
        raise ValueError("Invalid distance metric")

def kmeans(train_data, k, centroids, distance_metric='e2'):
    num_samples, num_features = len(train_data), len(train_data[0])
    old_centroids = [[0] * num_features for _ in range(k)]

    while old_centroids != centroids:
        old_centroids = [centroid.copy() for centroid in centroids]

        distances = [[calculate_distance(train_point, centroid, distance_metric) for centroid in centroids]
                     for train_point in train_data]

        labels = [min(range(k), key=lambda i: distances[j][i]) for j in range(num_samples)]

        for i in range(k):
            cluster_points = [train_data[j] for j in range(num_samples) if labels[j] == i]
            if cluster_points:
                centroids[i] = [sum(coord) / len(cluster_points) for coord in zip(*cluster_points)]

    return labels, centroids

def main():
    parser = argparse.ArgumentParser(description='Supervised learning Algorithms(kNN)')
    parser.add_argument('-train', required = True, help='Training file path')
    parser.add_argument('-d', choices=['e2', 'manh'], help='Distance function for kMeans (Euclidean squared or Manhattan)')
    parser.add_argument('centroids', nargs='*',type=lambda x: list(map(int, x.split(','))), help='Centroids for kMeans (required for extra credit)')
    parser.add_argument('-k', type = int, default = 0, help='Number of neighbors for kNN(0 for naive bayes)')
    args = parser.parse_args()
    train_data = []
    train_labels = []
    
    with open(args.train, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            train_data.append(list(map(int, row[:-1])))
            train_labels.append(row[-1])

    if args.d:
        
        centroids = args.centroids
        kmeans_labels, centroids = kmeans(train_data, 3, centroids, args.d)
        print('kMeans Clustering Results:')
        for i in range(len(centroids)):
            cluster_points = [('A' + str(j+1)) for j in range(len(kmeans_labels)) if kmeans_labels[j] == i]
            
            print(f'Cluster C{i + 1}: {cluster_points}')
        for centroid in centroids:
            print(centroid)

if __name__ == '__main__':
    main()