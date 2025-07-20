import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient

# Підвантажуємо креди, коннектимось до дб та перевіряємо з'єднання
load_dotenv()

uri = os.getenv("MONGO_URI")
client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    exit(1)

db = client.book

# Перш ніж працювати з колекцією, дамо юзеру можливість наповнити її даними (з виключенням створення дублікатів)
def create_cat(name, age, features):
    cat = {
        "name": name,
        "age": age,
        "features": features
    }
    try:
        existing = db.cats.find_one(cat)
        if existing:
            print("Cat with the same name, age and features already exists.")
            return
        result = db.cats.insert_one(cat)
        print(f"Cat created with id: {result.inserted_id}")
    except Exception as e:
        print("Error creating cat:", e)

# Функція видачі списку усіх котів
def read_all():
    try:
        result = db.cats.find({})
        for el in result:
            print(el)
    except Exception as e:
        print("Error reading all cats:", e)

# Функція пошуку кота за ім'ям
def read_one(name):
    try:
        result = db.cats.find_one({"name": name})
        if result:
            print(result)
        else:
            print(f"No cat found with name: {name}")
    except Exception as e:
        print("Error reading cat:", e)

# Функція оновлення віку кота за ім'ям
def update_age(name, age):
    try:
        result = db.cats.update_one({"name": name}, {"$set": {"age": age}})
        if result.modified_count > 0:
            print(f"Updated age for {name} to {age}")
        else:
            print(f"No cat found with name: {name} or age is already {age}")
    except Exception as e:
        print("Error updating age:", e)

# Функція додавання нової фічі за ім'ям з перевіркою чи фіча вже існує
def add_feature(name, features):
    try:
        cat = db.cats.find_one({"name": name})
        if not cat:
            print(f"No cat found with name: {name}")
            return
        added_features = []
        for f in features:
            result = db.cats.update_one({"name": name}, {"$addToSet": {"features": f}})
            if result.modified_count > 0:
                added_features.append(f)
        if added_features:
            for f in added_features:
                print(f"Added feature '{f}' to {name}")
        else:
            print(f"The feature(s) already exist for {name}")
    except Exception as e:
        print("Error adding features:", e)

# Функція видалення запису для одного кота за ім'ям
def delete_cat(name):
    try:
        result = db.cats.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Deleted cat with name: {name}")
        else:
            print(f"No cat found with name: {name}")
    except Exception as e:
        print("Error deleting cat:", e)

# Функція видалення усіх записів з колекції
def delete_all():
    try:
        result = db.cats.delete_many({})
        print(f"Deleted {result.deleted_count} cats from the database")
    except Exception as e:
        print("Error deleting all cats:", e)

# Головна функція для взаємодії з користувачем
def main():
    while True:
        user_input = input("Enter command (create, read_all, read_one, update_age, add_feature, delete_cat, delete_all, exit): ").strip().lower()
        if user_input == "create":
            name = input("Enter cat name: ")
            age = int(input("Enter cat age: "))
            features = [f.strip() for f in input("Enter features: ").split(",")]
            create_cat(name, age, features)
        elif user_input == "read_all":
            read_all()
        elif user_input == "read_one":
            name = input("Enter cat name: ")
            read_one(name)
        elif user_input == "update_age":
            name = input("Enter cat name: ")
            age = int(input("Enter new age: "))
            update_age(name, age)
        elif user_input == "add_feature":
            name = input("Enter cat name: ")
            feature = [f.strip() for f in input("Enter feature(s) to add (comma-separated): ").split(",")]
            add_feature(name, feature)
        elif user_input == "delete_cat":
            name = input("Enter cat name: ")
            delete_cat(name)
        elif user_input == "delete_all":
           delete_all()
        elif user_input == "exit":
            print("Bye!")
            break
        else:
            print("Invalid command")


if __name__ == "__main__":
    main()