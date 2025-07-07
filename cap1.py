# Importing necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Loading the dataset (replace with your dataset)
# Example: 'financial_data.csv' should have features and a target column for prediction
data = pd.read_csv('financial_data.csv')

# Assuming 'target' is the column with risk labels (e.g., '0' for low risk, '1' for high risk)
X = data.drop(columns=['target'])
y = data['target']

# Splitting the dataset into training and testing sets (80-20 split)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) 

# Training and evaluating Support Vector Machine (SVM)
svm_model = SVC(kernel='linear')  # You can experiment with other kernels like 'rbf'
svm_model.fit(X_train, y_train)
svm_pred = svm_model.predict(X_test)

# Evaluate SVM model
print("SVM Model Evaluation:")
print("Accuracy: ", accuracy_score(y_test, svm_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, svm_pred))
print("Classification Report:\n", classification_report(y_test, svm_pred))

# Training and evaluating Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)

# Evaluate Random Forest model
print("\nRandom Forest Model Evaluation:")
print("Accuracy: ", accuracy_score(y_test, rf_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, rf_pred))
print("Classification Report:\n", classification_report(y_test, rf_pred))

# You can also compare the models' performance and select the one with the best accuracy or other relevant metrics.
