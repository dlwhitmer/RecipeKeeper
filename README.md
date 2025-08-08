# 🧾 Recipe Keeper

Recipe Keeper is a modular desktop application built with PyQt6, designed to help users manage their personal recipe collection with ease. Featuring a clean UI and full CRUD functionality, it’s perfect for home cooks, food bloggers, or anyone who wants a smarter way to organize their culinary creations.

---

## 🚀 Features

- **Create Recipes**  
  Add new recipes with titles, ingredients, and instructions using an intuitive form.

- **Read Recipes**  
  Browse and view saved recipes in a scrollable list. Each recipe displays its full details.

- **Update Recipes**  
  Edit existing recipes with a single click. Fields populate automatically for easy modification.

- **Delete Recipes**  
  Remove unwanted recipes instantly with confirmation to prevent accidental deletion.

- **Responsive UI**  
  Dynamic layouts, tooltips, and elided text ensure a polished user experience.

- **Modular Architecture**  
  Clean separation of concerns using reusable components and embedded widgets.

---

## 🧪 Usage

1. Launch the app.
2. Click **New Recipe** to create a new entry.
3. Select a recipe from the list to **View**, **Edit**, or **Delete**.
4. Changes are saved automatically to the local SQLite database.

---

## 🛠️ Tech Stack

| Component      | Description                          |
|----------------|--------------------------------------|
| **PyQt6**      | GUI framework for building the interface |
| **SQLite**     | Lightweight database for recipe storage |
| **Python3**     | Core application logic and data handling |

---

## 📦 Installation

```bash
git clone https://github.com/dlwhitmer/RecipeKeeper
cd recipe-keeper
pip install -r requirements.txt
python main.py
