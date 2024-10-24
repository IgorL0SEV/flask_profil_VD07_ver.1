from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'some_secret_key'
profiles_file = 'profiles.json'


# Функция для загрузки профилей из файла
def load_profiles():
    if os.path.exists(profiles_file):
        with open(profiles_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


# Функция для сохранения профилей в файл
def save_profiles(profiles):
    with open(profiles_file, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, ensure_ascii=False, indent=4)


# Маршрут для отображения списка профилей
@app.route('/')
def profiles():
    users = load_profiles()
    return render_template('profiles.html', users=users)


# Маршрут для редактирования профиля
@app.route('/edit_profile/<int:user_id>', methods=['GET', 'POST'])
def edit_profile(user_id):
    users = load_profiles()
    user = next((u for u in users if u['id'] == user_id), None)

    if request.method == 'POST':
        if user:
            user['name'] = request.form['name']
            user['email'] = request.form['email']
            user['password'] = request.form['password']
            save_profiles(users)  # Сохраняем обновленные данные в файл
            flash('Изменения успешно сохранены!')
        return redirect(url_for('profiles'))

    return render_template('edit_profile.html', user=user)


# Маршрут для добавления нового профиля
@app.route('/new_profile', methods=['GET', 'POST'])
def new_profile():
    users = load_profiles()

    if request.method == 'POST':
        new_id = max([u['id'] for u in users]) + 1 if users else 1
        new_user = {
            'id': new_id,
            'name': request.form['name'],
            'email': request.form['email'],
            'password': request.form['password']
        }
        users.append(new_user)
        save_profiles(users)  # Сохраняем обновленные данные в файл
        flash('Новый профиль успешно добавлен!')
        return redirect(url_for('profiles'))

    return render_template('edit_profile.html', user={})


# Маршрут для удаления профиля
@app.route('/delete_profile/<int:user_id>', methods=['POST'])
def delete_profile(user_id):
    users = load_profiles()
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        users.remove(user)
        save_profiles(users)
        flash(f'Профиль {user["name"]} удалён!')
    return redirect(url_for('profiles'))


if __name__ == '__main__':
    app.run(debug=True)

