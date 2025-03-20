import math
import pandas as pd
from graphviz import Digraph

# --- Fungsi ID3 Murni ---

def entropy(labels):
    """
    Menghitung entropy dari sekumpulan label.
    """
    freq = labels.value_counts()
    total = len(labels)
    ent = 0.0
    for count in freq:
        p = count / total
        ent -= p * math.log2(p)
    return ent

def information_gain(data, feature, target):
    """
    Menghitung information gain dari pemilihan 'feature' untuk memisahkan 'target'.
    """
    original_entropy = entropy(data[target])
    values = data[feature].unique()
    weighted_entropy = 0.0
    for val in values:
        subset = data[data[feature] == val]
        weighted_entropy += (len(subset) / len(data)) * entropy(subset[target])
    return original_entropy - weighted_entropy

def id3(data, target, features=None):
    """
    Membangun pohon keputusan ID3 secara rekursif.
    """
    if features is None:
        features = list(data.columns)
        features.remove(target)
    
    # Jika semua data memiliki label yang sama, kembalikan label tersebut (leaf node)
    if len(data[target].unique()) == 1:
        return data[target].iloc[0]
    
    # Jika tidak ada fitur tersisa, kembalikan label mayoritas
    if len(features) == 0:
        return data[target].value_counts().idxmax()
    
    best_feature = None
    best_ig = -1
    for f in features:
        ig = information_gain(data, f, target)
        if ig > best_ig:
            best_ig = ig
            best_feature = f
    
    tree = {best_feature: {}}
    feature_values = data[best_feature].unique()
    remaining_features = [f for f in features if f != best_feature]
    
    for val in feature_values:
        subset = data[data[best_feature] == val]
        if len(subset) == 0:
            tree[best_feature][val] = data[target].value_counts().idxmax()
        else:
            tree[best_feature][val] = id3(subset, target, remaining_features)
    
    return tree

def predict(tree, sample):
    """
    Melakukan prediksi satu sample menggunakan pohon ID3.
    """
    if not isinstance(tree, dict):
        return tree
    feature = list(tree.keys())[0]
    feature_value = sample.get(feature)
    subtree = tree[feature].get(feature_value)
    if subtree is None:
        return None
    return predict(subtree, sample)

def print_tree(tree, indent=""):
    """
    Menampilkan pohon keputusan dalam format teks (untuk debugging / cek struktur).
    """
    if not isinstance(tree, dict):
        print(indent + "└── " + str(tree))
        return
    feature = list(tree.keys())[0]
    print(indent + str(feature))
    for val, subtree in tree[feature].items():
        print(indent + f" ├── [{val}] -> ", end="")
        if isinstance(subtree, dict):
            print()
            print_tree(subtree, indent + " |     ")
        else:
            print(str(subtree))


# --- Contoh Data Training ---
data_training = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 0, 0, 0, 1, 1],
    [0, 1, 0, 0, 1, 0, 0, 0, 1],
    [0, 1, 0, 0, 1, 0, 0, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 1, 1, 0, 0, 1, 0],
    [0, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 1, 1, 1, 0, 1, 0]
]

columns = [
    'Kehamilan<=3', 
    'GulaDarah>120', 
    'TekananDarah<=60',
    'KetebalanKulit>30', 
    'Insulin>100', 
    'BMI>35',
    'RiwayatDiabetes>1', 
    'Umur<=45',
    'Hasil'
]

df = pd.DataFrame(data_training, columns=columns)

# Bangun pohon keputusan ID3 murni
tree_id3 = id3(df, target='Hasil')

print("Pohon Keputusan (ID3 Murni) - Format Teks:")
print_tree(tree_id3)


# --- Fungsi Visualisasi Pohon Dengan Graphviz ---

def visualize_tree(tree, graph_name="ID3_Tree", rankdir="TB"):
    """
    Mengubah pohon keputusan (dictionary) menjadi visualisasi menggunakan graphviz.
    rankdir: "TB" (top to bottom) atau "LR" (left to right).
    """
    dot = Digraph(name=graph_name, comment="ID3 Decision Tree",
                  graph_attr={"rankdir": rankdir, "splines": "ortho"})
    
    # Anda bisa mengatur atribut global node/edge di sini
    dot.node_attr.update(
        fontname="Arial",
        fontsize="12",
    )
    dot.edge_attr.update(
        fontname="Arial",
        fontsize="10",
    )

    counter = 0  # counter untuk ID unik setiap node
    
    def add_nodes_edges(subtree, parent=None, edge_label=""):
        nonlocal counter
        
        # Jika leaf node (bukan dictionary), tambahkan node daun
        if not isinstance(subtree, dict):
            leaf_id = f"leaf_{counter}"
            dot.node(leaf_id, label=str(subtree),
                     shape="box", style="filled", color="#8cd3ff")  # warna biru muda
            if parent is not None:
                dot.edge(parent, leaf_id, label=edge_label)
            counter += 1
            return
        
        # Decision node
        feature = list(subtree.keys())[0]
        node_id = f"node_{counter}"
        dot.node(node_id, label=feature,
                 shape="ellipse", style="filled", color="#cfcfcf")  # warna abu-abu terang
        if parent is not None:
            dot.edge(parent, node_id, label=edge_label)
        counter += 1
        
        # Tambahkan anak-anak
        for val, child in subtree[feature].items():
            add_nodes_edges(child, parent=node_id, edge_label=str(val))
    
    add_nodes_edges(tree)
    return dot


# Membuat visualisasi pohon
dot_tree = visualize_tree(tree_id3, graph_name="ID3_Tree", rankdir="TB")

# Menyimpan dan menampilkan
dot_tree.render("ID3_Tree_Visualization", format="png", view=True)
