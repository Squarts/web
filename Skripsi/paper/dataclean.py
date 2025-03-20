import pandas as pd
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

# 1. Membaca data
df = pd.read_csv("diabetes.csv")

# 2. Menghapus baris dengan nilai 0 pada kolom
critical_columns = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "Age"]
df_clean = df[(df[critical_columns] != 0).all(axis=1)]

# 3. Memisahkan atribut dan label
X = df_clean.drop("Outcome", axis=1)
y = df_clean["Outcome"]

# 4. Split data menjadi train dan test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Terapkan SMOTE hanya pada data training
smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

# Export balanced data to CSV
balanced_data = pd.DataFrame(X_train_balanced, columns=X.columns)
balanced_data['Outcome'] = y_train_balanced
balanced_data.to_csv("dataset.csv", index=False)