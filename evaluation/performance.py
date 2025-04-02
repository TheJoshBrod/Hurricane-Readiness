# Read in lists
official = []
official_value = []
predicted = []

with open("list.txt", "r") as file:
    for line in file:
        line = line.strip()
        official.append(line.split(":")[1])
        official_value.append(float(line.split(":")[2][1:]))

with open("predicted_list.txt", "r") as file:
    for line in file:
        line = line.strip()
        predicted.append(line.split(":")[1])

# Kendall Tau
pairs = set()
for i in range(len(official)):
    for j in range(i+1, len(official)):
        pairs.add((official[i], official[j]))

x = 0
y = 0
for i in range(len(predicted)):
    for j in range(i+1, len(predicted)):
        if (predicted[i], predicted[j]) in pairs:
            x += 1
        else:
            y += 1

ktd = (x - y) / (x + y)

# Top K Precision / Accuracy
# Counties with over 200 loss per person is considered relevant
relevant_threshold = 200
relevant = set()
for i in range(len(official_value)):
    if official_value[i] >= relevant_threshold:
        relevant.add(official[i])

k_values = [5, 10, 25, 50, 100, 200]
precision = []
recall = []
for k in k_values:
    tp = 0
    for i in range(k):
        if predicted[i] in relevant:
            tp += 1
    precision.append(tp / k)
    recall.append(tp / len(relevant))

with open('metrics.txt', 'w') as f:
    f.write("Kendall tau distance: " + str(ktd) + "\n\n")
    for i in range(len(k_values)):
        f.write("Top " + str(k_values[i]) + " predicted counties\n")
        f.write("\tPrecision: " + str(precision[i]) + "\n")
        f.write("\tRecall: " + str(recall[i]) + "\n")