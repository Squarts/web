import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# Langkah 1: Membersihkan data
df = pd.read_csv("dataset.csv")

# 2. Memisahkan fitur dan target
X = df.drop('Outcome', axis=1)
y = df['Outcome']

# 3. Membangi data testing menjadi 0.2
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=42)

# 4. Membuat model Decision Tree ID3
model = DecisionTreeClassifier(
    criterion='entropy',
    random_state=42,
    max_depth=3  # Membatasi cabang untuk visualisasi lebih baik
)
model.fit(X_train, y_train)

# 5. Evaluasi akurasi
y_pred = model.predict(X_test)
scores = cross_val_score(model, X, y, cv=10, scoring='accuracy')
print(f"Akurasi: {scores.mean()}%")

# 6. Visualisasi pohon keputusan
plt.figure(figsize=(20,10))
plot_tree(
    model,
    feature_names=X.columns,
    class_names=['Non-Diabetes', 'Diabetes'],
    filled=True,
    rounded=True,
    fontsize=9
)
plt.show()