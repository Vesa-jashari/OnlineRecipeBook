import pandas as pd
import streamlit as st
import requests
import pandas
from dotenv import load_dotenv
import os

from unicodedata import category

load_dotenv()

Api_base_url = os.getenv("api_base_url")


def get_categories():
    response = requests.get(f"{Api_base_url}/categories")
    return response.json()


def get_recipes(cuisine=None, difficulty=None):
    param = {}
    if cuisine:
        param["cuisine"] = cuisine

    if difficulty:
        param["difficulty"] = difficulty

    response = requests.get(f"{Api_base_url}/recipes", params=param)

    return response.json()


def create_category(category_name):
    responses = requests.post(
        f"{Api_base_url}/categories", json={"name": category_name})
    return responses.json()


def update_category(category_id, category_name):
    response = requests.put(
        f"{Api_base_url}/categories/{category_id}", json={"name": category_name})
    return response.json()


def delete_category(category_id):
    response = requests.delete(f"{Api_base_url}/categories/{category_id}")
    return response.json()


def create_recipes(recipe_name, description, ingredients, instructions, cuisine, difficulty, category_id):
    response = requests.post(f"{Api_base_url}/recipes", json={
        "name": recipe_name,
        "description": description,
        "ingredients": ingredients,
        "instructions": instructions,
        "cuisine": cuisine,
        "difficulty": difficulty,
        "category_id": category_id
    })
    return response.json()


def update_recipe(recipe_id, recipe_name, description, ingredients, instructions, cuisine, difficulty, category_id):
    response = requests.put(f"{Api_base_url}/recipes/{recipe_id}", json={
        "name": recipe_name,
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


st.title("Online Recipe Book")
menu=["Dashboard","Manage Recipes","Manage Categories"]
selected_menu=st.sidebar.selectbox("Menu",menu)
if selected_menu=="Dashboard":
    st.header("Dashboard")
    st.subheader("Recipes")
    recipe_list=get_recipes()
    if recipe_list:
        df_recipes=pd.DataFrame(recipe_list)
        if "id" in df_recipes.columns:
            df_recipes=df_recipes.drop(columns=["id"])
            df_recipes.reset_index(drop=True, inplace=True)
            df_recipes.index+=1
            st.dataframe(df_recipes, use_container_width=True)
    else:
        st.info("no recipes found")

    st.subheader("Categories")
    category_list=get_categories()
    if category_list:
        df_categories=pd.DataFrame(category_list)
        if "id" in df_categories.columns:
            df_categories=df_categories.drop(columns=["id"])
            df_categories.reset_index(drop=True, inplace=True)
            df_categories.index+=1
            st.dataframe(df_categories,use_container_width=True)
        else:
            st.info("No categories found")

    elif selected_menu=="Manage Recipes":
        st.header("Manage Recipes")
        st.subheader("Add a new Recipe")
        recipe_name=st.text_input("Recipe Name" ,key="new_recipe_name")
        recipe_description=st.text_input("Recipe description",key="new_recipe_description")
        recipe_ingredients = st.text_input("Recipe ingredients", key="new_recipe_ingredients")
        recipe_instructions=st.text_input("Recipe instructions",key="new_instructions")
        recipe_cuisine = st.text_input("Recipe cuisine", key="new_recipe_cuisine")
        recipe_difficulty = st.text_input( "Difficulty",["Easy","Medium","Hard"], key="new_recipe_difficulty")
        category_list=get_categories()
        if category_list:
            category_name=[cat["name"] for cat in category_list]
            selected_category_name=st.selectbox("Category", category_name,key="new_recipe_category")
            selected_category_id=next(cat["id"] for cat in category_list if cat["name"]==selected_category_name)
        else:
            st.error("Failed to retrieve categories")
            selected_category_id=None
        if st.button("Add Recipe", key="add_recipe_button"):
            if (all([recipe_name,recipe_ingredients,recipe_cuisine,recipe_instructions,recipe_difficulty,selected_category_id is not None]))
                create_recipes(recipe_name,recipe_description,recipe_ingredients,recipe_instructions,selected_category_id)
                st.success(f"Recipe{recipe_name} added successfully")
            else:
                st.error("All fields must be filled and category selected to add a recipe")
        st.subheader("Edit or delete recipe")
        recipe_list=get_recipes()
        if recipe_list:
            recipe_name=[recipe["name"] for recipe in recipe_list]
            manage_action=st.radio("Choose action",["Edit","Delete"],key="edit_recipe_select")
            if manage_action=="Edit":
                recipe_edit=st.selectbox("Select a recipe to edit",recipe_name,key="edit_recipe_select")
                if recipe_edit:
                    selected_recipe=next(recipe for recipe in recipe_list if recipe["name"]==recipe_edit)
                    st.subheader(f"Edit recipe:{selected_recipe['name']}")
                    edit_name=st.text_input("Recipe Name", value=selected_recipe["name"],key="edit_recipe_name")
                    edit_description = st.text_input("Description", value=selected_recipe["description"], key="edit_recipe_description")
                    edit_ingredients = st.text_input("ingredients", value=selected_recipe["ingredients"], key="edit_recipe_ingredients")
                    edit_cuisine = st.text_input("cuisine", value=selected_recipe["cuisine"], key="edit_recipe_cuisine")
                    edit_instructions = st.text_input("instructions", value=selected_recipe["instructions"], key="edit_recipe_instructions")
                    edit_difficulty=st.selectbox("Difficulty",["Easy","Medium","Hard"],index=["Easy","Medium","Hard"].index(selected_recipe["difficulty"]),key="edit_recipe_difficulty"
                    category_list=get_categories()
                    if category_list:
                        category_names=[cat["name"] for cat in category_list]
                        edit_category_name=st.selectbox("Category",category_names,index=category_name.index(next(cat["name"] for cat in category_list if cat ["id"]==selected_recipe["category_list"]))
                        edit_recipe_id=next(cat["id"] for cat in category_list if cat["name"]==edit_category_name)
                    else:
                        st.error("Failed to retrieve categories")
                        edit_category_id=None

                    if st.button("Update recipe",key="update_recipe_button"):
                         if all([edit_name,edit_instructions,edit_description.edit_ingredients)])


                    else:
                         st.error("all fields must be filled out")
                elif manage_action=="Delete":
                    recipe_to_delete=st.selectbox("Select a recipe to delete")




    else:
         st.info("No recipe available to manage")
elif selected_menu=="Manage Categories":
    st.header("Manage categories")
    st.subheader("Add a new Category")
    new_category_name=st.text_input("New Category Name", key="new_category_name")
    if st.button("Add Category",key="add_category_button"):
        if new_category_name:
            create_category(new_category_name)
            st.sucess(f"Category created")
        else:













         if st.button("Update Category",key="update_category+_button"):
             if new_category_name:
