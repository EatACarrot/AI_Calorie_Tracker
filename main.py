import os
import tkinter as tk
import datetime
from os import system as os_system
from dotenv import load_dotenv
from xai_sdk import Client
from xai_sdk.chat import user, system
from enum import Enum

from typing import TypedDict

class Ingreadient:
    def __init__(self, name: str) -> None:
        self.calories: float = 0
        self.macros = TypedDict('macros', {
            'protein': float,
            'carbohydrates': float,
            'fats': float
        })
        self.name: str = name
        
    def __str__(self) -> str:
        return f'    -{self.name} has {self.calories}kcal'
    
        
class Meal:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.date = datetime.datetime.now()
        self.ingredients: list[Ingreadient] = []
        self.total_calories: float = 0
        self.total_macros = TypedDict('total_macros', {
            'protein': float,
            'carbohydrates': float,
            'fats': float
        })
        self.promptString: str = ""
        
    def addIngredient(self, ingredient: Ingreadient) -> None:
        self.ingredients.append(ingredient)
        
    def Remove_ingredient(self, ingredient: Ingreadient) -> None:
        self.ingredients.remove(ingredient)
        
    def __str__(self) -> str:
        return f'{self.name} has {self.total_calories}kcal and here is the break down: '


def Tk_page_history(meals: list[Meal], root) -> tk.Frame:
    frame = tk.Frame(root)
    for meal in meals:
        m_label = tk.Label(frame, text=meal, font=("Arial", 12), height=1, width=40)
        m_label.pack(side='top', expand=False, fill='none', anchor='nw')
        i = 0
        for ingredient in meal.ingredients:
            i_frame = tk.Frame(frame)
            i_label = tk.Label(i_frame, text=ingredient, font=("Arial", 8), height=1, width=40)
            i_label.pack(side='left', expand=False, fill='none',anchor='nw')
            i_del_button = tk.Button(i_frame, text="-", command=lambda ml=meal, ing=ingredient, i_f=i_frame: (ml.Remove_ingredient(ing), i_f.destroy()))
            i_del_button.pack(side='left')
            i_frame.pack(side='top')
            i += 1
    frame.grid(row=1, column=0, columnspan= 2)
    return frame
    

def Tk_add_Ingredient(list: list[tk.Entry], root) -> None:
    ing_label = tk.Label(root, text=f'Nr.{len(list) + 1}:')
    ing_label.pack(side='top')
    ing_entry = tk.Entry(root)
    ing_entry.pack(side='top')
    list.append(ing_entry)

def Tk_add_meal_entry(list_of_entries: list[tk.Entry], meals: list[Meal], name_entry: tk.Entry) ->None:
    meal_name = name_entry.get()
    if meal_name is None or not meal_name.strip():
        return
    meal = Meal(meal_name)
    for entry in list_of_entries:
        ing_name = entry.get()
        if ing_name is None or not ing_name.strip():
            continue
        ingredient = Ingreadient(ing_name)
        meal.addIngredient(ingredient)
    meals.append(meal)
        
def Tk_page_add(meals: list[Meal], root) -> tk.Frame:
    print("used open_function")
    frame = tk.Frame(root)
    ingredient_list: list = []
    m_label = tk.Label(frame, text=f'Food description')
    m_label.pack(side='top')
    m_entry = tk.Entry(frame)
    m_entry.pack(side='top')
    add_more_ingredients = tk.Button(frame, text=f'Add Ingredient', command=lambda:Tk_add_Ingredient(list=ingredient_list, root=frame))
    add_more_ingredients.pack(side='top')
    add_meal = tk.Button(frame, text=f'Add the Meal', command=lambda:Tk_add_meal_entry(list_of_entries=ingredient_list, meals=meals, name_entry=m_entry))
    add_meal.pack(side='bottom')
    frame.grid(row=1, column=0, columnspan= 2)
    return frame

class visual_continer:
    class Page(Enum):
        HISTORY = 1
        ADD = 2
            
    def __init__(self, meals: list[Meal], root: tk.Tk):
        self.root = root
        self.meals = meals
        
        self.frame_history = Tk_page_history(meals=meals, root=root)
        self.frame_history.grid(row=1, column=0, columnspan= 2)
        
        self.frame_add = None
        
        b_history = tk.Button(root, text=f'History', command=lambda: self.Open_window(open_function=Tk_page_history, open_page=self.Page.HISTORY))
        b_history.grid(row=0, column=0)
        b_add = tk.Button(root, text=f'Add', command=lambda: self.Open_window(open_function=Tk_page_add, open_page=self.Page.ADD))
        b_add.grid(row=0, column=1)
    
    def Open_window(self, open_function, open_page: Page) -> None:
        match open_page:
            case self.Page.ADD:
                if self.frame_history is not None:
                    self.frame_history.destroy()
                    self.frame_history = None
                if self.frame_add is None:
                    self.frame_add = open_function(self.meals, self.root)
                    self.frame_add.grid(row=1, column=0, columnspan= 2)
            case _:
                if self.frame_add is not None:
                    self.frame_add.destroy()
                    self.frame_add = None
                if self.frame_history is None:
                    self.frame_history = open_function(self.meals, self.root)
                    self.frame_history.grid(row=1, column=0, columnspan= 2)
            
            

        
meals: list[Meal] = [Meal(f'{x} meal') for x in range(0,3)]
for meal in meals:
    for x in range(0,6):
        meal.addIngredient(Ingreadient(f'ingredient nr.{x}'))
#for meal in meals:
    #print(meal)
    

root = tk.Tk() 
root.title("Calorie Tracker")
root.geometry("800x600")
app_gui = visual_continer(meals=meals,root=root)
root.mainloop()

#load_dotenv(".env")
#client = Client(api_key = os.getenv("XAI_API_KEY"))

#chat = client.chat.create(model="grok-4-1-fast-reasoning")
#chat.append(system("You are Grok, a highly intelligent, helpful AI assistant."))
#chat.append(user("What is the meaning of life, the universe, and everything?"))
#response = chat.sample()
#print(response.content)