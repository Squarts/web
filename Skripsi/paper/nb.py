import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import accuracy_score
from sklearn.inspection import permutation_importance

# 1. Membaca data
df = pd.read_csv("dataset.csv")

# 2. Memisahkan atribut dan label
X = df.drop('Outcome', axis=1)
y = df['Outcome']

# 3. Membangi data testing menjadi 0.2
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=42)

# 4. Membuat dan melatih model
model = GaussianNB()
model.fit(X_train, y_train)

# 5. Evaluasi model
y_pred = model.predict(X_test)
scores = cross_val_score(model, X, y, cv=10, scoring='accuracy')
print(f"\nAkurasi: {scores.mean()}%")

# 6. Permutation Importance
results = permutation_importance(
    model, 
    X_test, 
    y_test,
    n_repeats=10,
    random_state=42
)

# Buat DataFrame importance
feature_importance = pd.DataFrame({
    'Atribut': X.columns,
    'Pengaruh': results.importances_mean
}).sort_values('Pengaruh', ascending=False)

print("\nFaktor Paling Berpengaruh terhadap Diabetes:")
print(feature_importance.to_string(index=False))

# 7. Menampilkan 10 Hasil Prediksi
sample_data = X_test.iloc[:10].copy()
sample_data['Aktual'] = y_test.iloc[:10].values
sample_data['Prediksi'] = y_pred[:10]

# Menampikan no 
sample_data.reset_index(drop=True, inplace=True)

# Tampilkan semua fitur
print("\nHasil Lengkap prediksi 10 Data Testing:")
print(sample_data)