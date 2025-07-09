import pyodbc
from typing import List, Dict

# SQL Server bağlantı bilgileri
server = 'DESKTOP-H6SIL9M\SQLEXPRESS'
database = 'Akakce'


def get_products() -> List[Dict]:
    conn = None
    cursor = None
    products = []
    try:
        conn = pyodbc.connect(
            f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = conn.cursor()

        cursor.execute("""
            SELECT Name, Price, Seller, Product_Type, Brand
            FROM Table_Arcelik
        """)
        rows = cursor.fetchall()

        for row in rows:
            products.append({
                "name": row[0],
                "price": row[1],
                "seller": row[2],
                "product_type": row[3],
                "brand": row[4]
            })
        print("Veritabanından başarıyla veri çekildi.")
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"!!! Veritabanı Bağlantı/Sorgu Hatası: {sqlstate} - {ex}")
        return [] # Hata durumunda boş liste döndür
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return products

# Ana test bloğu
if __name__ == "__main__":
    print("Veritabanı bağlantı testi başlatılıyor...")
    data = get_products()

    if data:
        print(f"\nÇekilen {len(data)} adet ürün bulundu:")
        for product in data:
            print(f"- Ad: {product['name']}, Fiyat: {product['price']}, Satıcı: {product['seller']}, Tür: {product['product_type']}, Marka: {product['brand']}")
    else:
        print("\n!!! Veritabanından hiçbir ürün çekilemedi veya bir hata oluştu.")
        print("Lütfen SQL Server'daki 'Akakce' veritabanındaki 'Table_Arcelik' tablosunda veri olup olmadığını ve bağlantı izinlerini kontrol edin.")