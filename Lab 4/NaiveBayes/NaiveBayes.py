import argparse
import csv
from collections import defaultdict

def evaluate(predictions, actual_labels):
    labels = set(actual_labels)
    results = []

    for label in labels:
        true_positives = sum(1 for pred, actual in zip(predictions, actual_labels) if pred == label and actual == label)
        false_positives = sum(1 for pred, actual in zip(predictions, actual_labels) if pred == label and actual != label)
        false_negatives = sum(1 for pred, actual in zip(predictions, actual_labels) if pred != label and actual == label)

        precision_numerator = true_positives
        precision_denominator = true_positives + false_positives
        recall_numerator = true_positives
        recall_denominator = true_positives + false_negatives

        precision = f"{precision_numerator}/{precision_denominator}" if precision_denominator > 0 else "0/0"
        recall = f"{recall_numerator}/{recall_denominator}" if recall_denominator > 0 else "0/1"

        result_line = f"Label={label} Precision={precision} Recall={recall}"
        results.append(result_line)
    return results


def naive_bayes(train_data, train_labels, test_data, laplacian_constant=1):
    class_probs = {}
    feature_probs = defaultdict(lambda: defaultdict(int))

    unique_labels = []
    for label in train_labels:
        if label not in unique_labels:
            unique_labels.append(label)

    total_samples = len(train_labels)
    for label in unique_labels:
        class_probs[label] = (train_labels.count(label)) / (total_samples)
        label_data = [train_data[i] for i in range(len(train_labels)) if train_labels[i] == label]
        A0 = 0
        A1 = 0
        A2 = 0
        for i in range(len(label_data)):
            if label_data[i][0] == 1:
                A0 = A0 + 1
            if label_data[i][1] == 1:
                A1 = A1 + 1
            if label_data[i][2] == 1:
                A2 = A2 + 1  
        
        feature_probs[label][0] = ( A0 + laplacian_constant) / (len(label_data) + 2 * laplacian_constant)
        feature_probs[label][1] = ( A1 + laplacian_constant) / (len(label_data) + 2 * laplacian_constant)
        feature_probs[label][2] = ( A2 + laplacian_constant) / (len(label_data) + 2 * laplacian_constant)
        
    
    predictions = []
    for test_point in test_data:
        label_scores = {}
        for label in unique_labels:
            likelihood = class_probs[label]*((feature_probs[label][0]) if test_point[0] == 1 else (1 - (feature_probs[label][0]))) * ((feature_probs[label][1]) if test_point[1] == 1 else (1 - (feature_probs[label][1])))* ((feature_probs[label][2]) if test_point[2] == 1 else (1 - (feature_probs[label][2])))
            label_scores[label] =  likelihood
            
        
        predicted_label = max(label_scores, key=label_scores.get)
        predictions.append(predicted_label)

    return predictions

def main():
    parser = argparse.ArgumentParser(description='Supervised learning Algorithms(KNN)')
    parser.add_argument('-train', required = True, help='Training file path')
    parser.add_argument('-test', required = True, help = 'Test file path')
    parser.add_argument('-c', type=int, default=0, help='Laplacian correction for Naive Bayes')    
    
    args = parser.parse_args()
    train_data = []
    train_labels = []
    c = args.c
    with open(args.train, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            train_data.append(list(map(int, row[:-1])))
            train_labels.append(str(row[-1]))
    
    test_data =[]
    test_labels = []
    with open(args.test, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            test_data.append(list(map(int, row[:-1])))
            test_labels.append(str(row[-1]))
    
    predictions = naive_bayes(train_data, train_labels, test_data, c)

    labels = set(test_labels)
    
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