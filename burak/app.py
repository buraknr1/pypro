import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def reset_database():
    conn = sqlite3.connect('/home/mustafaburakbayram/mysite/quiz.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS sorular')
    conn.commit()
    conn.close()

def create_database():
    conn = sqlite3.connect('/home/mustafaburakbayram/mysite/quiz.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sorular (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            soru TEXT,
            secenek_a TEXT,
            secenek_b TEXT,
            secenek_c TEXT,
            secenek_d TEXT,
            dogru_cevap TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_questions():
    questions = [
        ("Python'da AI geliştirme için hangi kütüphane yaygın olarak kullanılır?", "a) NumPy", "b) Matplotlib", "c) Keras", "d) Pandas", "c"),
        ("Flask nedir?", "a) Web Framework", "b) Veri Analizi Kütüphanesi", "c) Makine Öğrenimi Kütüphanesi", "d) Oyun Motoru", "a"),
        ("Derin öğrenme modellerini eğitmek için hangi kütüphane kullanılır?", "a) Scikit-Learn", "b) TensorFlow", "c) BeautifulSoup", "d) Flask", "b"),
        ("Flask'ta route tanımlamak için hangi decorator kullanılır?", "a) @app.route", "b) @flask.route", "c) @route", "d) @app.path", "a"),
        ("Hangi kütüphane doğal dil işleme için kullanılır?", "a) NumPy", "b) SciPy", "c) NLTK", "d) Matplotlib", "c")
    ]

    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.executemany('''
        INSERT INTO sorular (soru, secenek_a, secenek_b, secenek_c, secenek_d, dogru_cevap) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', questions)
    conn.commit()
    conn.close()


def get_questions():
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('SELECT * FROM sorular')
    questions = c.fetchall()
    conn.close()
    return questions

@app.route('/')
def home():
    questions = get_questions()
    return render_template('quiz.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    questions = get_questions()
    score = 0
    for question in questions:
        q_id = str(question[0])
        if request.form.get(f'q{q_id}') == question[6]:
            score += 1
    return f'Skorunuz: {score}'

if __name__ == '__main__':
    reset_database()
    create_database()
    insert_questions()
    app.run(debug=True)