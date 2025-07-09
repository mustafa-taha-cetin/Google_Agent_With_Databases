# ---------------------------- Ana Kütüphane İçe Aktarımları ----------------------------
import pyodbc
from typing import List, Dict
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext



# ------------------- SQL Server bağlantı bilgileri -------------------

server = 'DESKTOP-H6SIL9M\SQLEXPRESS'
database = 'Akakce'




# --- Ürünleri Veritabanından Çekme Fonksiyonu ---

def get_products() -> List[Dict]:
    """
    SQL Server'daki 'Table_Arcelik' tablosundan ürün bilgilerini çeker.
    Bağlantı hatalarını yakalar ve ürün listesini döndürür.
    """
    conn = None
    cursor = None
    products = []
    try:
        conn = pyodbc.connect(
            f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = conn.cursor()

        # Sorguyu çalıştır
        cursor.execute("""
            SELECT Name, Price, Seller, Product_Type, Brand
            FROM Table_Arcelik
        """)
        rows = cursor.fetchall()

        # Çekilen veriyi listeye dönüştür
        for row in rows:
            products.append({
                "name": row[0],
                "price": row[1],
                "seller": row[2],
                "product_type": row[3],
                "brand": row[4]
            })

    except pyodbc.Error as ex:
        # Veritabanı bağlantısı veya sorgu hatası durumunda hata mesajını yazdır
        sqlstate = ex.args[0]
        print(f"Database error: {sqlstate} - {ex}")
        # Hata durumunda boş liste döndür veya duruma göre özel bir hata fırlat
        return []
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return products




# ---------------------------- Data Base Agent Tanımı ----------------------------
data_base_agent = Agent(

    model='gemini-2.0-flash-001',

    name='data_base_agent',

    description="""A helpful assistant for collecting or selecting data in
    local databases; also, this agent can pull all data from databases.""",

    tools=[get_products],

    # Ajana hangi durumda hangi aracı kullanacağını belirten talimat

    instruction="""If the user asks for products or data from the database,
                   use the 'get_products' tool to retrieve them.
                   After fetching, present the product details including
                   Name, Price, Seller, Product Type, and Brand in a clear, readable list format.
                   If no products are found, inform the user that no products were found in the database.
                   For any other questions, respond politely that this agent specializes in database queries."""

)

root_agent = data_base_agent


