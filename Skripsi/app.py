import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine, MetaData, Table, insert, text
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import bcrypt
# Konfigurasi Flask
app = Flask(__name__)
app.secret_key = 'key'  # Secret key untuk sesi pengguna

# Konfigurasi database
db_user = 'root'
db_password = ''
db_host = 'localhost'
db_name = 'diabetes'
engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}')

# Membuat sesi untuk melakukan operasi database
Session = sessionmaker(bind=engine)
session_db = Session()

# Menyiapkan tabel inputdata dan dataset
metadata = MetaData()
metadata.reflect(bind=engine)
inputdata_table = metadata.tables.get('inputdata')
dataset_table = metadata.tables.get('dataset')

query = "SELECT pregnancies, glucose, blood, skin, insulin, bmi, dpf, age, outcome FROM dataset"
data = pd.read_sql(query, engine)

X = data.iloc[:, :-1]
y = data.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

naive_bayes_model = GaussianNB()
naive_bayes_model.fit(X_train, y_train)
id3_model = DecisionTreeClassifier(criterion='entropy', random_state=42)
id3_model.fit(X_train, y_train)

# Halaman Login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Ambil data pengguna berdasarkan username
        query = text("SELECT * FROM user WHERE username=:username")
        with engine.connect() as conn:
            result = conn.execute(query, {"username": username}).mappings().fetchone()

        if result:
            stored_password = result['password']  # Hasil sudah berupa dict
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                session['username'] = username
                return redirect(url_for('welcome'))
            else:
                error = "Password salah!"
        else:
            error = "Username tidak ditemukan!"

        return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        #Konfirmasi password
        if password != confirm_password:
            error = "Password dan konfirmasi password tidak cocok!"
            return render_template('register.html', error=error)

        # Periksa apakah username sudah ada di database
        query = text("SELECT * FROM user WHERE username=:username")
        with engine.connect() as conn:
            result = conn.execute(query, {"username": username}).fetchone()

        if result:
            error = "Username sudah digunakan, silakan pilih username lain."
            return render_template('register.html', error=error)

        # Hash password sebelum disimpan
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Simpan pengguna baru ke database
        stmt = text("INSERT INTO user (username, password) VALUES (:username, :password)")
        with engine.connect() as conn:
            conn.execute(stmt, {"username": username, "password": hashed_password.decode('utf-8')})
            conn.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Hapus username dari sesi
    return redirect(url_for('login'))  # Arahkan kembali ke halaman login

# Halaman Welcome setelah login
@app.route('/welcome')
def welcome():
    if 'username' not in session:
        return redirect(url_for('login'))  # Jika belum login, arahkan ke halaman login
    
    username = session['username']  # Ambil username dari sesi
    return render_template('welcome.html', username=username)  # Render halaman datang.html

# Halaman untuk form input data prediksi
@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    nb_accuracy = None
    id3_accuracy = None
    result = None
    saran = None
    if request.method == 'POST':
        try:
            pregnancies = int(request.form['pregnancies'])
            glucose = int(request.form['glucose'])
            blood = int(request.form['blood'])
            skin = int(request.form['skin'])
            insulin = int(request.form['insulin'])
            height_cm = float(request.form['height'])  # Konversi cm ke meter
            height_m = height_cm / 100
            weight = float(request.form['weight'])
            bmi = weight / (height_m ** 2)  # Rumus BMI
            dpf_numeric = int(request.form['dpf'])     # Ambil nilai 1 atau 0
            dpf = "Ya" if dpf_numeric == 1 else "Tidak"
            age = int(request.form['age'])
            outcome = 0
            algorithm = request.form['algorithm']

            # Persiapan input data
            input_data = scaler.transform([[pregnancies, glucose, blood, skin, insulin, bmi, dpf_numeric, age]])

            # Algoritma prediksi dan akurasi
            if algorithm == 'naive_bayes':
                prediction = naive_bayes_model.predict(input_data)
                naive_bayes_scores = cross_val_score(naive_bayes_model, X, y, cv=10, scoring='accuracy')
                nb_accuracy = naive_bayes_scores.mean()
            elif algorithm == 'id3':
                prediction = id3_model.predict(input_data)
                id3_scores = cross_val_score(id3_model, X, y, cv=10, scoring='accuracy')
                id3_accuracy = id3_scores.mean()

            # Ubah outcome menjadi string "diabetes" atau "tidak"
            outcome_str = "Diabetes" if prediction == 1 else "Negatif"

            current_time = datetime.now()

            # insert data ke tabel inputdata
            stmt = insert(inputdata_table).values(
                pregnancies=pregnancies,
                glucose=glucose,
                blood=blood,
                skin=skin,
                insulin=insulin,
                weight=weight,
                height=height_cm,
                bmi=bmi,
                dpf=dpf,
                age=age,
                outcome=outcome_str,
                algorithm=algorithm,
                nb_accuracy=nb_accuracy if algorithm == 'naive_bayes' else None,
                id3_accuracy=id3_accuracy if algorithm == 'id3' else None,
                username=username,  # Simpan username yang login
                waktu=current_time
            )
            with engine.connect() as conn:
                conn.execute(stmt)
                conn.commit()

            # Prediction results and suggestions
            if prediction == 1:
                result = outcome_str
                saran = """
                <h3>Solusi untuk Diabetes Positif</h3>
                <ul>
                    <li><b>Pola Makan:</b> Hindari makanan tinggi gula dan karbohidrat sederhana. Konsumsi lebih banyak sayuran, buah rendah gula, protein tanpa lemak, dan biji-bijian utuh.</li>
                    <li><b>Aktivitas Fisik:</b> Lakukan olahraga rutin minimal 30 menit per hari, seperti berjalan cepat, berenang, atau yoga.</li>
                    <li><b>Pemeriksaan Rutin:</b> Periksa gula darah secara teratur untuk memantau kadar gula dan konsultasikan perkembangan dengan dokter spesialis.</li>
                    <li><b>Manajemen Stres:</b> Kurangi stres melalui teknik relaksasi seperti meditasi, yoga, atau terapi konseling.</li>
                    <li><b>Obat-Obatan:</b> Minum obat atau insulin sesuai resep dokter untuk mengontrol kadar gula darah.</li>
                    <li><b>Hidrasi:</b> Konsumsi air putih yang cukup untuk menjaga metabolisme tubuh.</li>
                </ul>
                """
            else:
                result = outcome_str
                saran = """
                <h3>Solusi untuk Diabetes Negatif</h3>
                <ul>
                    <li><b>Pola Makan:</b> Jaga pola makan seimbang dengan asupan sayuran, buah, dan serat yang cukup.</li>
                    <li><b>Aktivitas Fisik:</b> Tetap aktif secara fisik untuk menjaga berat badan ideal dan kesehatan jantung.</li>
                    <li><b>Pemeriksaan Berkala:</b> Lakukan tes kesehatan secara rutin untuk mendeteksi risiko diabetes atau penyakit lainnya lebih awal.</li>
                    <li><b>Hindari Gula Berlebih:</b> Kurangi konsumsi gula tambahan dan makanan olahan untuk mencegah risiko di masa depan.</li>
                    <li><b>Hindari Stres Berlebihan:</b> Manajemen stres melalui hobi atau aktivitas sosial dapat membantu menjaga kesehatan mental dan fisik.</li>
                </ul>
                """

            return render_template('index.html', result=result, saran=saran, nb_acc=nb_accuracy, id3_acc=id3_accuracy)
        
        except Exception as e:
            print(f"Error: {e}")
            return render_template('index.html', result="Error ketika melakukan prediksi", saran=None)

    return render_template('index.html', result=None, saran=None, nb_acc=None, id3_acc=None)

# Halaman history setelah inputdata
@app.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    
    # Query untuk mendapatkan data berdasarkan pengguna
    query = f"SELECT * FROM inputdata WHERE username='{username}'"
    user_data = pd.read_sql(query, engine)

    user_data['accuracy'] = user_data.apply(lambda row: row['nb_accuracy'] if row['algorithm'] == 'naive_bayes' else row['id3_accuracy'], axis=1)
    
    return render_template('history.html', username=username, user_data=user_data)

# Rute untuk update data pada history
@app.route('/update/<int:record_id>', methods=['GET', 'POST'])
def update(record_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']

    # Ambil data berdasarkan ID
    query = f"SELECT * FROM inputdata WHERE id={record_id} AND username='{username}'"
    with engine.connect() as conn:
        record = conn.execute(text(query)).fetchone()

    if request.method == 'POST':
        try:
            pregnancies = int(request.form['pregnancies'])
            glucose = int(request.form['glucose'])
            blood = int(request.form['blood'])
            skin = int(request.form['skin'])
            insulin = int(request.form['insulin'])
            height_cm = float(request.form['height'])  # Tinggi dalam cm
            weight = float(request.form['weight'])     # Berat badan dalam kg
            height_m = height_cm / 100                # Konversi tinggi ke meter
            bmi = weight / (height_m ** 2)            # Hitung BMI
            dpf_numeric = int(request.form['dpf'])     # Nilai numerik DPF
            dpf = "Ya" if dpf_numeric == 1 else "Tidak"  # Konversi ke "Ya"/"Tidak"
            age = int(request.form['age'])
            algorithm = request.form['algorithm']

            # Ubah data sesuai algoritma
            input_data = scaler.transform([[pregnancies, glucose, blood, skin, insulin, bmi, dpf_numeric, age]])

            if algorithm == 'naive_bayes':
                prediction = naive_bayes_model.predict(input_data)
                naive_bayes_scores = cross_val_score(naive_bayes_model, X, y, cv=10, scoring='accuracy')
                nb_accuracy = naive_bayes_scores.mean()
                id3_accuracy = None
            elif algorithm == 'id3':
                prediction = id3_model.predict(input_data)
                id3_scores = cross_val_score(id3_model, X, y, cv=10, scoring='accuracy')
                id3_accuracy = id3_scores.mean()
                nb_accuracy = None

            outcome = "Diabetes" if prediction == 1 else "Negatif"

            # Update data di database
            update_query = text("""
                UPDATE inputdata
                SET pregnancies=:pregnancies, glucose=:glucose, blood=:blood, skin=:skin, 
                    insulin=:insulin, height=:height, weight=:weight, bmi=:bmi, dpf=:dpf, 
                    age=:age, algorithm=:algorithm,nb_accuracy=:nb_accuracy, id3_accuracy=:id3_accuracy ,outcome=:outcome, waktu=:waktu
                WHERE id=:record_id AND username=:username
            """)

            current_time = datetime.now()

            with engine.connect() as conn:
                conn.execute(update_query, {
                    'pregnancies': pregnancies, 'glucose': glucose, 'blood': blood, 'skin': skin,
                    'insulin': insulin, 'height': height_cm, 'weight': weight, 'bmi': bmi, 'dpf': dpf,
                    'age': age, 'algorithm': algorithm,'nb_accuracy': nb_accuracy, 'id3_accuracy': id3_accuracy,'waktu': current_time,
                    'outcome': outcome, 'record_id': record_id, 'username': username
                })
                conn.commit()

            return redirect(url_for('history'))

        except Exception as e:
            print(f"Error: {e}")
            return "Terjadi kesalahan saat memperbarui data."

    return render_template('update.html', record=record)

# Rute untuk menghapus data dari history
@app.route('/delete/<int:record_id>', methods=['GET', 'POST'])
def delete(record_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']  # Ambil username dari sesi
    
    # Hapus data dari database
    delete_query = text("""DELETE FROM inputdata WHERE id=:record_id AND username=:username""")
    with engine.connect() as conn:
        conn.execute(delete_query, {'record_id': record_id, 'username': username})
        conn.commit()

    return redirect(url_for('history'))

if __name__ == '__main__':
    app.run(debug=True)
