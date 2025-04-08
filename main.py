import os
from datetime import datetime
import psycopg2
import psycopg2.extras
#postgresql databazasini ulash
def get_connection():
    return psycopg2.connect(
        host="localhost",
        user="postgres",
        password="postgres",
        database="oop"
    )
#Item classi(Vorislik berish uchun Ota klass)
class Item:
    def __init__(self, name, item_type, parent_id, absolute_path, size):
        self.name = name
        self.type = item_type
        self.parent_id = parent_id
        self.absolute_path = absolute_path
        self.size = size
#Saqlash
    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO items (name, type, parent_id, absolute_path, size) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (self.name, self.type, self.parent_id, self.absolute_path, self.size))
        conn.commit()
        conn.close()
# Yaratilgan hamma file va directoryni olish va ko'rsatish uchun funksiya
    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM items WHERE deleted_at IS NULL")
        result = cursor.fetchall()
        conn.close()
        return [dict(row) for row in result]

# Update qilish funksiyasi
    @staticmethod
    def update(item_id, new_name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE items SET name = %s WHERE id = %s", (new_name, item_id))
        conn.commit()
        conn.close()

# O'chirish uchun funksiya
    @staticmethod
    def delete(item_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE items SET deleted_at = %s WHERE id = %s", (datetime.now(), item_id))
        conn.commit()
        conn.close()

# File classini yaratish
class File(Item):
    def __init__(self, name,parent_id, absolute_path, size):
        super().__init__(name,'file', parent_id, absolute_path, size)

# Directory classini yaratish
class Directory(Item):
    def __init__(self, name, parent_id, absolute_path):
        super().__init__(name,'directory', parent_id, absolute_path, size=0)

# Ekranga chiqarish uchun
while True:
    print("\n1. Fayl yaratish\n2. Katalog yaratish\n3. Ko‘rish\n4. Yangilash\n5. O‘chirish\n6. Chiqish")
    choice = input("Tanlang: ")
# File objektini yaratish
    if choice == '1':
        name = input("Fayl nomi: ")
        parent = input("Parent ID (yo‘q bo‘lsa None): ") or None
        path = input("To‘liq yo‘li: ")
        if os.path.isfile(path):
            size = os.path.getsize(path)
            file = File(name, parent, path, size)
            file.save()
            print(f"Fayl bazaga saqlandi. Hajmi: {size} bayt")
        else:
            print("Bunday fayl mavjud emas. Iltimos, to‘g‘ri yo‘l kiriting.")
# Katalog objectini yaratish
    elif choice == '2':
        name = input("Katalog nomi: ")
        parent = input("Parent ID (yo‘q bo‘lsa None): ") or None
        path = input("To‘liq yo‘li: ")
        directory = Directory(name, parent, path)
        directory.save()
# Yaratilgan file va directorylarni ko'rish
    elif choice == '3':
        items = Item.get_all()
        for i in items:
            print(i)
# Yaratilgan objectni yangilash
    elif choice == '4':
        id = input("ID: ")
        new_name = input("Yangi nom: ")
        Item.update(id, new_name)
# Objectni o'chirish
    elif choice == '5':
        id = input("O‘chirish uchun ID: ")
        Item.delete(id)
# Funksiyani tugatish
    elif choice == '6':
        break
# menyuda yo'q buyruq berilsa qaytadan menyu chiqadi
    else:
        continue