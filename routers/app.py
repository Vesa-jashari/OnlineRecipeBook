import pandas as pd
import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# API Base URL from environment variables
Api_base_url = os.getenv("api_base_url")


# Utility Functions
def get_categories():
    response = requests.get(f"{Api_base_url}/categories")
    if response.ok:
        return response.json()
    return []


def get_recipes(cuisine=None, difficulty=None):
    params = {}
    if cuisine:
        params["cuisine"] = cuisine
    if difficulty:
        params["difficulty"] = difficulty

    response = requests.get(f"{Api_base_url}/recipes", params=params)
    if response.ok:
        return response.json()
    return []


def create_category(category_name):
    response = requests.post(f"{Api_base_url}/categories", json={"name": category_name})
    return response.json()


def update_category(category_id, category_name):
    response = requests.put(
        f"{Api_base_url}/categories/{category_id}", json={"name": category_name}
    )
    return response.json()


def delete_category(category_id):
    response = requests.delete(f"{Api_base_url}/categories/{category_id}")
    return response.json()


def create_recipe(name, description, ingredients, instructions, cuisine, difficulty, category_id):
    response = requests.post(f"{Api_base_url}/recipes", json={
        "name": name,
        "description": description,
        "ingredients": ingredients,
        "instructions": instructions,
        "cuisine": cuisine,
        "difficulty": difficulty,
        "category_id": category_id
    })
    return response.json()


def update_recipe(recipe_id, name, description, ingredients, instructions, cuisine, difficulty, category_id):
    response = requests.put(f"{Api_base_url}/recipes/{recipe_id}", json={
        "name": name,
        "description": description,
        "ingredients": ingredients,
        "instructions": instructions,
        "cuisine": cuisine,
        "difficulty": difficulty,
        "category_id": category_id
    })
    return response.json()


def delete_recipe(recipe_id):
    response = requests.delete(f"{Api_base_url}/recipes/{recipe_id}")
    return response.json()


# Streamlit App
st.title("Online Recipe Book")

menu = ["Dashboard", "Manage Recipes", "Manage Categories"]
selected_menu = st.sidebar.selectbox("Menu", menu)

if selected_menu == "Dashboard":
    st.header("Dashboard")

    # Display Recipes
    st.subheader("Recipes")
    recipe_list = get_recipes()
    if recipe_list:
        df_recipes = pd.DataFrame(recipe_list)
        if "id" in df_recipes.columns:
            df_recipes = df_recipes.drop(columns=["id"])
        st.dataframe(df_recipes, use_container_width=True)
    else:
        st.info("No recipes found.")

    # Display Categories
    st.subheader("Categories")
    category_list = get_categories()
    if category_list:
        df_categories = pd.DataFrame(category_list)
        if "id" in df_categories.columns:
            df_categories = df_categories.drop(columns=["id"])
        st.dataframe(df_categories, use_container_width=True)
    else:
        st.info("No categories found.")

elif selected_menu == "Manage Recipes":
    st.header("Manage Recipes")

    # Add a New Recipe
    st.subheader("Add a New Recipe")
    recipe_name = st.text_input("Recipe Name", key="new_recipe_name")
    recipe_description = st.text_area("Description", key="new_recipe_description")
    recipe_ingredients = st.text_area("Ingredients", key="new_recipe_ingredients")
    recipe_instructions = st.text_area("Instructions", key="new_recipe_instructions")
    recipe_cuisine = st.text_input("Cuisine", key="new_recipe_cuisine")
    recipe_difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="new_recipe_difficulty")
    category_list = get_categories()
    if category_list:
        category_name = [cat["name"] for cat in category_list]
        selected_category_name = st.selectbox("Category", category_name, key="new_recipe_category")
        selected_category_id = next(cat["id"] for cat in category_list if cat["name"] == selected_category_name)
    else:
        st.error("Failed to retrieve categories.")
        selected_category_id = None

    if st.button("Add Recipe", key="add_recipe_button"):
        if all([recipe_name, recipe_description, recipe_ingredients, recipe_instructions, recipe_cuisine,
                recipe_difficulty, selected_category_id]):
            create_recipe(recipe_name, recipe_description, recipe_ingredients, recipe_instructions, recipe_cuisine,
                          recipe_difficulty, selected_category_id)
            st.success(f"Recipe '{recipe_name}' added successfully!")
        else:
            st.error("All fields must be filled to add a recipe.")

    # Manage Recipes
    st.subheader("Edit or Delete Recipes")
    recipe_list = get_recipes()
    if recipe_list:
        recipe_name_list = [recipe["name"] for recipe in recipe_list]
        manage_action = st.radio("Choose Action", ["Edit", "Delete"], key="manage_recipe_action")

        if manage_action == "Edit":
            recipe_to_edit = st.selectbox("Select a Recipe to Edit", recipe_name_list, key="edit_recipe_select")
            if recipe_to_edit:
                selected_recipe = next(recipe for recipe in recipe_list if recipe["name"] == recipe_to_edit)

                edit_name = st.text_input("Recipe Name", value=selected_recipe["name"], key="edit_recipe_name")
                edit_description = st.text_area("Description", value=selected_recipe["description"],
                                                key="edit_recipe_description")
                edit_ingredients = st.text_area("Ingredients", value=selected_recipe["ingredients"],
                                                key="edit_recipe_ingredients")
                edit_instructions = st.text_area("Instructions", value=selected_recipe["instructions"],
                                                 key="edit_recipe_instructions")
                edit_cuisine = st.text_input("Cuisine", value=selected_recipe["cuisine"], key="edit_recipe_cuisine")
                edit_difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"],
                                               index=["Easy", "Medium", "Hard"].index(selected_recipe["difficulty"]),
                                               key="edit_recipe_difficulty")

                if st.button("Update Recipe", key="update_recipe_button"):
                    update_recipe(selected_recipe["id"], edit_name, edit_description, edit_ingredients,
                                  edit_instructions, edit_cuisine, edit_difficulty, selected_recipe["category_id"])
                    st.success(f"Recipe '{edit_name}' updated successfully!")

        elif manage_action == "Delete":
            recipe_to_delete = st.selectbox("Select a Recipe to Delete", recipe_name_list, key="delete_recipe_select")
            if recipe_to_delete:
                selected_recipe = next(recipe for recipe in recipe_list if recipe["name"] == recipe_to_delete)
                if st.button("Delete Recipe", key="delete_recipe_button"):
                    delete_recipe(selected_recipe["id"])
                    st.success(f"Recipe '{selected_recipe['name']}' deleted successfully.")

    else:
        st.info("No recipes available to manage.")

elif selected_menu == "Manage Categories":
    st.header("Manage Categories")

    # Add a New Category
    st.subheader("Add a New Category")
    new_category_name = st.text_input("Category Name", key="new_category_name")
    if st.button("Add Category", key="add_category_button"):
        if new_category_name:
            create_category(new_category_name)
            st.success(f"Category '{new_category_name}' created successfully!")
        else:
            st.error("Category name cannot be empty.")

    # Manage Categories
    st.subheader("Edit or Delete Categories")
    category_list = get_categories()
    if category_list:
        category_name_list = [cat["name"] for cat in category_list]
        manage_action = st.radio("Choose Action", ["Edit", "Delete"], key="manage_category_action")

        if manage_action == "Edit":
            category_to_edit = st.selectbox("Select a Category to Edit", category_name_list, key="edit_category_select")
            if category_to_edit:
                selected_category = next(cat for cat in category_list if cat["name"] == category_to_edit)
                edit_category_name = st.text_input("Category Name", value=selected_category["name"],
                                                   key="edit_category_name")
                if st.button("Update Category", key="update_category_button"):
                    update_category(selected_category["id"], edit_category_name)
                    st.success(f"Category '{edit_category_name}' updated successfully!")

        elif manage_action == "Delete":
            category_to_delete = st.selectbox("Select a Category to Delete", category_name_list,
                                              key="delete_category_select")
            if category_to_delete:
                selected_category = next(cat for cat in category_list if cat["name"] == category_to_delete)
                if st.button("Delete Category", key="delete_category_button"):
                    delete_category(selected_category["id"])
                    st.success(f"Category '{selected_category['name']}' deleted successfully.")

    else:
        st.info("No categories available to manage.")
