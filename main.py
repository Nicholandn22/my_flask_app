from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Koneksi ke database RDS
def get_db_connection():
    return mysql.connector.connect(
        host='db-robopark.crtxsdecqcur.us-east-1.rds.amazonaws.com',
        user='admin',
        password='Boss1all23',
        database='mydb'
    )

@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Query untuk mendapatkan jumlah data yang masuk hari ini
    query_today = "SELECT COUNT(*) AS total_today FROM person WHERE DATE(dataCreated) = CURDATE();"
    
    # Eksekusi query dan pengambilan data
    cursor.execute(query_today)
    total_today = cursor.fetchone()[0]  # Ambil nilai total

    # Ambil data untuk emotion, usia, dan gender
    query_emotion = "SELECT emotion, COUNT(*) FROM person GROUP BY emotion"
    query_usia = "SELECT usia, COUNT(*) FROM person GROUP BY usia"
    query_gender = "SELECT gender, COUNT(*) FROM person GROUP BY gender"
    
    cursor.execute(query_emotion)
    emotions = cursor.fetchall()
    cursor.execute(query_usia)
    usia_data = cursor.fetchall()
    cursor.execute(query_gender)
    gender_data = cursor.fetchall()

    # Format data untuk JSON
    data = {
        'total_today': total_today,
        'emotions': {'labels': [row[0] for row in emotions], 'values': [row[1] for row in emotions]},
        'usia': {'labels': [row[0] for row in usia_data], 'values': [row[1] for row in usia_data]},
        'gender': {'labels': [row[0] for row in gender_data], 'values': [row[1] for row in gender_data]}
    }

    cursor.close()
    connection.close()

    return render_template('index2.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
