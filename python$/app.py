from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

# تحميل المتغيرات من ملف .env
load_dotenv()

app = Flask(__name__)

# إعدادات Telegram من المتغيرات البيئية
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# قائمة المستخدمين المسجلين
registered_users = {}
feedbacks = {}

# إرسال رسالة باستخدام Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, data=payload)
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        contact = request.form.get('contact')
        timestamp = datetime.now()
        user_id = len(registered_users) + 1
        registered_users[user_id] = {
            'name': name,
            'surname': surname,
            'contact': contact,
            'timestamp': timestamp
        }
        return redirect(url_for('feedback', user_id=user_id))
    return render_template('register.html')

@app.route('/feedback/<int:user_id>', methods=['GET', 'POST'])
def feedback(user_id):
    if request.method == 'POST':
        feedback = request.form.get('feedback')
        if user_id in registered_users:
            feedbacks[user_id] = feedback
            user_info = registered_users[user_id]
            message = (f"Feedback from {user_info['name']} {user_info['surname']} ({user_info['contact']}):\n"
                       f"{feedback}")
            send_telegram_message(message)
            return jsonify({'message': 'شكراً على رأيك!'})
        return jsonify({'message': 'المستخدم غير مسجل.'}), 400
    return render_template('feedback.html', user_id=user_id)

@app.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update(user_id):
    if user_id not in registered_users:
        return jsonify({'message': 'المستخدم غير مسجل.'}), 400
    user_info = registered_users[user_id]
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        contact = request.form.get('contact')
        timestamp = user_info['timestamp']
        if datetime.now() - timestamp > timedelta(minutes=1):
            return jsonify({'message': 'يمكنك تحديث معلوماتك بعد 1 دقيقة فقط.'}), 400
        registered_users[user_id] = {
            'name': name,
            'surname': surname,
            'contact': contact,
            'timestamp': timestamp
        }
        return jsonify({'message': 'تم تحديث المعلومات بنجاح!'})
    return render_template('update.html', user_info=user_info, user_id=user_id)

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/submit', methods=['POST'])
def submit_feedback():
    feedback = request.form['feedback']
    # إرسال الرأي إلى بوت التليجرام (تكملة الشيفرة الخاصة بك هنا)
    
    # توجيه المستخدم إلى صفحة تأكيد
    return render_template('confirmation.html')
