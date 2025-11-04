# Импорты
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Order
from weasyprint import HTML
import base64, io

# Создание приложения Flask
app = Flask(__name__, template_folder='../frontend/assets/Autentification/LoginRegistration', static_folder='../frontend/assets/index')
app.config['SECRET_KEY'] = 'group112-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Инициализация БД и LoginManager
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Загрузка пользователя
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Создание БД и суперадмина
with app.app_context():
    db.create_all()
    if not User.query.filter_by(login='Andrew').first():
        superadmin = User(login='Andrew', email='andrew@group-112.ru', phone='+79991234567', role='superadmin')
        superadmin.set_password('A.lampard@1234567')
        db.session.add(superadmin)
        db.session.commit()

# === Главная (фронтенд) ===
@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

# === Статические файлы ===
@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory('../frontend/assets/index', filename)

# === Логин ===
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        user = User.query.filter_by(login=login).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Неверный логин или пароль')
    return render_template('login.html')

# === Регистрация ===
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        if User.query.filter_by(login=login).first() or User.query.filter_by(email=email).first():
            flash('Логин или email уже заняты')
            return redirect(url_for('register'))
        user = User(login=login, email=email, phone=phone, role='user')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация успешна')
        return redirect(url_for('login'))
    return render_template('register.html')

# === Логаут ===
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# === Личный кабинет ===
@app.route('/dashboard')
@login_required
def dashboard():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('../Dashboard/dashboard.html', user=current_user, orders=orders)

# === Админ-панель ===
@app.route('/admin')
@login_required
def admin():
    if current_user.role not in ['admin', 'superadmin']:
        flash('Доступ запрещён')
        return redirect(url_for('dashboard'))
    orders = Order.query.all()
    users = User.query.all()
    return render_template('../Dashboard/admin.html', orders=orders, users=users)

# === Новая заявка ===
@app.route('/new-order', methods=['POST'])
@login_required
def new_order():
    service = request.form['service']
    description = request.form['description']
    cost = float(request.form['cost'])
    if current_user.balance < cost:
        flash('Недостаточно средств')
        return redirect(url_for('dashboard'))
    current_user.balance -= cost
    order = Order(user_id=current_user.id, service=service, description=description, cost=cost)
    db.session.add(order)
    db.session.commit()
    flash('Заявка создана')
    return redirect(url_for('dashboard'))

# === Назначить заказ ===
@app.route('/assign-order/<int:order_id>', methods=['POST'])
@login_required
def assign_order(order_id):
    if current_user.role not in ['admin', 'superadmin']:
        return 'Forbidden', 403
    order = Order.query.get(order_id)
    order.assigned_to = request.form['admin_id']
    order.status = 'in_progress'
    db.session.commit()
    return redirect(url_for('admin'))

# === PDF договор ===
@app.route('/generate-contract', methods=['POST'])
@login_required
def generate_contract():
    data = request.json
    html_str = render_template('../Dashboard/contract_template.html', **data)
    pdf = HTML(string=html_str).write_pdf()
    return send_file(io.BytesIO(pdf), download_name='dogovor.pdf', mimetype='application/pdf')

# Запуск
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003, debug=True)