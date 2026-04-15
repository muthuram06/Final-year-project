import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Load predicted file
predicted = pd.read_csv("behaviour_log.csv")

# Load ground truth file
true_data = pd.read_csv(r"C:\Final year project\Current Web Detection\data\test_labels.csv")
# Align by length (important)
min_len = min(len(predicted), len(true_data))

y_pred = predicted["predicted_label"][:min_len]
y_true = true_data["true_label"][:min_len]

accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

print("Accuracy:", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall:", round(recall, 4))
print("F1 Score:", round(f1, 4))

print("Confusion Matrix:")
print(confusion_matrix(y_true, y_pred))