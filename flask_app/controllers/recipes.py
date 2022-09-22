from flask import Flask, render_template, request, redirect, session
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

'''READ ALL'''
@app.route("/recipes")
def read_recipes():
    return render_template("recipes.html", output=Recipe.select_all())

'''READ ONE'''
@app.route("/recipe/<id>")
def read_recipe(id):
    data={"id": id}
    result = Recipe.select_one(data)
    return render_template("recipe.html", output = result)

'''CREATE'''
@app.route("/recipe/create")
def recipe_create():
    return render_template("recipe_create.html")

@app.route("/recipe/create/process", methods=["POST"])
def recipe_create_process():
    data = request.form
    Recipe.insert(data)
    return redirect("/recipes")

'''EDIT'''
@app.route("/recipe/<id>/update")
def recipe_update(id):
    data={"id": id}
    return render_template("recipe_edit.html", output = Recipe.select_one(data))

@app.route("/recipe/update/process", methods=["POST"])
def recipe_update_process():
    data={k:v for k,v in request.form.items()}
    data['instructions']=data['instructions'].strip()
    Recipe.update(data)
    return redirect(f"/dashboard")

'''DELETE'''
@app.route("/recipe/<id>/delete")
def delete_recipe(id):
    data={"id":id}
    Recipe.delete(data)
    return redirect("/recipes")
