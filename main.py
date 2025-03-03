from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage
users = {}
recipes = []

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/preferences', methods=['POST'])
def preferences():
    name = request.form.get('name')
    users[name] = {'dietary': '', 'cuisine': '', 'meals': 0}
    return render_template('preferences.html', name=name)

@app.route('/save_preferences', methods=['POST'])
def save_preferences():
    name = request.form.get('name')
    users[name]['dietary'] = request.form.get('dietary')
    users[name]['cuisine'] = request.form.get('cuisine')
    users[name]['meals'] = int(request.form.get('meals'))
    return redirect(url_for('recipe_input', name=name))

@app.route('/recipe_input', methods=['GET', 'POST'])
def recipe_input():
    name = request.args.get('name')
    if request.method == 'POST':
        recipe_name = request.form.get('recipe_name')
        ingredients = request.form.get('ingredients')
        recipes.append({'name': recipe_name, 'ingredients': ingredients, 'user': name})
    return render_template('recipe_input.html', name=name, recipes=recipes)

@app.route('/recipe_plan', methods=['GET'])
def recipe_plan():
    name = request.args.get('name')
    user_recipes = [r for r in recipes if r['user'] == name]
    return render_template('recipe_plan.html', name=name, recipes=user_recipes, user=users.get(name, {}))

if __name__ == '__main__':
    app.run(debug=True)
