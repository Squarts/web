import pandas as pd
import numpy as np
import math

# Baca data training dan testing
train_data = pd.read_csv('datatraining.csv')
test_data = pd.read_csv('datatesting.csv')

# Pisahkan fitur dan target
X_train = train_data.iloc[:, :-1]
y_train = train_data['Hasil']
test_instance = test_data.iloc[0, :-1].values

# Hitung prior probabilities
prior_positif = len(y_train[y_train == 'Positif']) / len(y_train)
prior_negatif = len(y_train[y_train == 'Negatif']) / len(y_train)

# Fungsi untuk menghitung Gaussian PDF
def gaussian_pdf(x, mean, std):
    exponent = math.exp(-((x - mean)**2 / (2 * std**2)))
    return (1 / (math.sqrt(2 * math.pi) * std)) * exponent

# Hitung statistik untuk setiap kelas
def calculate_class_stats(df):
    return {col: {'mean': df[col].mean(), 'std': df[col].std()} for col in df.columns}

positif_stats = calculate_class_stats(X_train[y_train == 'Positif'])
negatif_stats = calculate_class_stats(X_train[y_train == 'Negatif'])

# Hitung likelihood untuk satu instance
def calculate_likelihood(stats, instance):
    likelihood = 1
    for i, (feature, value) in enumerate(zip(stats.keys(), instance)):
        if stats[feature]['std'] == 0:  # Hindari division by zero
            stats[feature]['std'] = 1e-9
        likelihood *= gaussian_pdf(value, stats[feature]['mean'], stats[feature]['std'])
    return likelihood

# Hitung likelihood untuk kedua kelas
likelihood_positif = calculate_likelihood(positif_stats, test_instance)
likelihood_negatif = calculate_likelihood(negatif_stats, test_instance)

# Hitung posterior probabilities
posterior_positif = likelihood_positif * prior_positif
posterior_negatif = likelihood_negatif * prior_negatif

# Normalisasi
total_posterior = posterior_positif + posterior_negatif
prob_positif = posterior_positif / total_posterior
prob_negatif = posterior_negatif / total_posterior

# Hasil akhir
print(f"\nProbabilitas Positif: {prob_positif * 100:.4f}%")
print(f"Probabilitas Negatif: {prob_negatif * 100:.4f}%")
prediction = 'Positif' if prob_positif > prob_negatif else 'Negatif'
print(f"\nPrediksi: {prediction}")