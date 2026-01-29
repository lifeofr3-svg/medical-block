import pandas as pd
import numpy as np
import os

np.random.seed(42)

os.makedirs('Testing/diabetes_samples', exist_ok=True)
os.makedirs('Testing/heart_samples', exist_ok=True)

print("Creating 10 Diabetes sample CSV files...")

diabetes_samples = [
    [6, 148, 72, 35, 0, 33.6, 0.627, 50],
    [1, 85, 66, 29, 0, 26.6, 0.351, 31],
    [8, 183, 64, 0, 0, 23.3, 0.672, 32],
    [1, 89, 66, 23, 94, 28.1, 0.167, 21],
    [0, 137, 40, 35, 168, 43.1, 2.288, 33],
    [5, 116, 74, 0, 0, 25.6, 0.201, 30],
    [3, 78, 50, 32, 88, 31.0, 0.248, 26],
    [10, 115, 0, 0, 0, 35.3, 0.134, 29],
    [2, 197, 70, 45, 543, 30.5, 0.158, 53],
    [8, 125, 96, 0, 0, 0.0, 0.232, 54]
]

diabetes_columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

for i, sample in enumerate(diabetes_samples, 1):
    df = pd.DataFrame([sample], columns=diabetes_columns)
    filename = f'Testing/diabetes_samples/diabetes_sample_{i}.csv'
    df.to_csv(filename, index=False)
    print(f"Created: {filename}")

print("\nCreating 10 Heart Disease sample CSV files...")

heart_samples = [
    [63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1],
    [37, 1, 2, 130, 250, 0, 1, 187, 0, 3.5, 0, 0, 2],
    [41, 0, 1, 130, 204, 0, 0, 172, 0, 1.4, 2, 0, 2],
    [56, 1, 1, 120, 236, 0, 1, 178, 0, 0.8, 2, 0, 2],
    [57, 0, 0, 120, 354, 0, 1, 163, 1, 0.6, 2, 0, 2],
    [57, 1, 0, 140, 192, 0, 1, 148, 0, 0.4, 1, 0, 1],
    [56, 0, 1, 140, 294, 0, 0, 153, 0, 1.3, 1, 0, 2],
    [44, 1, 1, 120, 263, 0, 1, 173, 0, 0.0, 2, 0, 3],
    [52, 1, 2, 172, 199, 1, 1, 162, 0, 0.5, 2, 0, 3],
    [57, 1, 2, 150, 168, 0, 1, 174, 0, 1.6, 2, 0, 2]
]

heart_columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']

for i, sample in enumerate(heart_samples, 1):
    df = pd.DataFrame([sample], columns=heart_columns)
    filename = f'Testing/heart_samples/heart_sample_{i}.csv'
    df.to_csv(filename, index=False)
    print(f"Created: {filename}")

print("\n✅ All 20 sample CSV files created successfully!")
print("📁 Location: Testing/diabetes_samples/ and Testing/heart_samples/")