import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

# 1. Membaca data
df = pd.read_csv("dataset.csv")
X = df.drop("Outcome", axis=1)
y = df["Outcome"]

# 3. Membangi data testing menjadi 0.2
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Membuat dan melatih model
id3_model = DecisionTreeClassifier(criterion="entropy", random_state=42)
id3_model.fit(X_train, y_train)
nb_model = GaussianNB()
nb_model.fit(X_train, y_train)

# 5. Evaluasi model dengan 10-fold cross validation
scores_id3 = cross_val_score(id3_model, X_train, y_train, cv=10, scoring="accuracy")
scores_nb = cross_val_score(nb_model, X_train, y_train, cv=10, scoring="accuracy")
id3_mean_accuracy = scores_id3.mean() * 100
nb_mean_accuracy = scores_nb.mean() * 100

print("----------------------------------------")
print(f"Akurasi Rata-Rata (id3): {id3_mean_accuracy:.1f}%")
print(f"Akurasi Rata-Rata (nb): {nb_mean_accuracy:.1f}%")
print("----------------------------------------")
