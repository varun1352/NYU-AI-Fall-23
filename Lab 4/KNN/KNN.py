import argparse 
import csv
from scipy.spatial import distance
import math
from collections import Counter

def euclidean_distance(point1, point2):
    return sum(abs(x - y) for x, y in zip(point1, point2))


def kNN(train_data, train_labels, test_data, k):
    predictions = []
    for test_point in test_data:
        distances = [(euclidean_distance(test_point, train_data[i]), train_labels[i]) for i in range(len(train_data))]
        sorted_distances = sorted(distances, key=lambda x: x[0])[:k]

        weighted_votes = Counter()
        for distance, label in sorted_distances:
            if distance != 0:  # Avoid division by zero
                weight = 1 / distance
                weighted_votes[label] += weight
            else:
                distance = 0.0001
                weight = 1 / distance
                weighted_votes[label] += weight
        predicted_label = max(weighted_votes, key=weighted_votes.get)
        predictions.append(predicted_label)

    return predictions

def evaluate(predictions, actual_labels):
    correct = sum(1 for pred, actual in zip(predictions, actual_labels) if pred == actual)
    precision = correct / len(predictions)
    recall = correct / len(actual_labels)
    return precision, recall

def main():
    parser = argparse.ArgumentParser(description='Supervised learning Algorithms(Lab 4)')
    parser.add_argument('-train', required = True, help='Training file path')
    parser.add_argument('-test', required = True, help = 'Test file path')
    parser.add_argument('-k', type = int, default = 0, help='Number of neighbors for KNN(0 for naive bayes)')
    parser.add_argument('-C', type=int, default=0, help='Laplacian correction for Naive Bayes')
    parser.add_argument('-v', action='store_true', help='Verbose mode')
    parser.add_argument('-d', choices=['e2', 'manh'], help='Distance function for kMeans (Euclidean squared or Manhattan)')
    parser.add_argument('centroids', nargs='*', help='Centroids for kMeans (required for extra credit)')
    
    args = parser.parse_args()
    train_data = []
    train_labels = []
    k = args.k
    with open(args.train, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            train_data.append(list(map(int, row[:-1])))
            train_labels.append(row[-1])
    
    test_data =[]
    test_labels = []
    with open(args.test, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            test_data.append(list(map(int, row[:-1])))
            test_labels.append(row[-1])
    
    predictions = kNN(train_data, train_labels, test_data, k)
    for actual_label, prediction in zip(test_labels, predictions):  
        print('want = ', actual_label, 'got = ', prediction)

    labels = set(predictions)
    print(labels)
    results = []
    
    for label in labels:
        true_positives = sum(1 for pred, actual in zip(predictions, test_labels) if pred == label and actual == label)
        false_positives = sum(1 for pred, actual in zip(predictions, test_labels) if pred == label and actual != label)
        false_negatives = sum(1 for pred, actual in zip(predictions, test_labels) if pred != label and actual == label)

        precision = f"{true_positives}/{true_positives + false_positives}" if true_positives + false_positives > 0 else "0"
        recall = f"{true_positives}/{true_positives + false_negatives}" if true_positives + false_negatives > 0 else "0"

        results.append(f"Label={label} Precision={precision} Recall={recall}")

    for result in results:
        print(result)
if __name__ == '__main__':
    main()