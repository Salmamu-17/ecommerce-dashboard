import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile
import os
import streamlit as st

# Judul Dashboard
st.title("Proyek Analisis Data: E-Commerce Public Dataset")

# Mendefinisikan relative path ke file ZIP (untuk penggunaan lokal)
import os

# Mendefinisikan relative path ke file ZIP (untuk penggunaan lokal)
zip_file_path = os.path.join(os.path.dirname(__file__), "data", "E-commerce-public-dataset.zip")  # Folder data harus berisi ZIP file


# Ekstrak file ZIP ke folder temp jika belum diekstrak
if not os.path.exists('temp'):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall("temp")

# Mendefinisikan relative path ke folder CSV setelah diekstrak
csv_folder = os.path.join("temp", "E-Commerce Public Dataset")

# Baca file CSV dari folder temp
df_customers = pd.read_csv(os.path.join(csv_folder, 'customers_dataset.csv'))
df_geolocation = pd.read_csv(os.path.join(csv_folder, 'geolocation_dataset.csv'))
df_items = pd.read_csv(os.path.join(csv_folder, 'order_items_dataset.csv'))
df_payments = pd.read_csv(os.path.join(csv_folder, 'order_payments_dataset.csv'))
df_reviews = pd.read_csv(os.path.join(csv_folder, 'order_reviews_dataset.csv'))
df_orders = pd.read_csv(os.path.join(csv_folder, 'orders_dataset.csv'))
df_products = pd.read_csv(os.path.join(csv_folder, 'products_dataset.csv'))
df_sellers = pd.read_csv(os.path.join(csv_folder, 'sellers_dataset.csv'))

# Data Wrangling
df_items_products = pd.merge(df_items, df_products, on='product_id')
df_items_orders = pd.merge(df_items_products, df_orders, on='order_id')
df_items_reviews = pd.merge(df_items_orders, df_reviews, on='order_id', how='left')
df_items_customers = pd.merge(df_items_reviews, df_customers, on='customer_id')

df_final = df_items_customers.copy()

# Cleaning Data
df_final['review_score'] = df_final['review_score'].fillna(0)
df_final = df_final.dropna(subset=['product_category_name', 'customer_city'])

# Pertanyaan 1: Pola Pembelian
st.header("Pertanyaan 1: Pola Pembelian Berdasarkan Kategori Produk dan Lokasi Geografis")

# Visualisasi distribusi pembelian berdasarkan kategori produk
# Set style for seaborn
sns.set(style="whitegrid")

# Visualisasi distribusi pembelian berdasarkan kategori produk
plt.figure(figsize=(25, 15))  # Ukuran figure yang lebih besar
sns.countplot(data=df_final, x='product_category_name', order=df_final['product_category_name'].value_counts().index)
plt.title('Distribusi Pembelian Berdasarkan Kategori Produk', fontsize=18)
plt.xlabel('Kategori Produk', fontsize=14)
plt.ylabel('Jumlah Pembelian', fontsize=14)

# Menambahkan label sumbu x dengan rotasi dan alignment
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.subplots_adjust(bottom=0.25)  # Menambahkan ruang di bawah plot

# Menyimpan plot ke Streamlit
st.pyplot(plt)

# Pertanyaan 2: Ulasan Konsumen Berdasarkan Produk yang Paling Banyak Dibeli
st.header("Pertanyaan 2: Ulasan Konsumen Berdasarkan Produk yang Paling Banyak Dibeli")

top_products = df_final['product_id'].value_counts().head(10).index
df_top_products = df_final[df_final['product_id'].isin(top_products)]

# Visualisasi rata-rata ulasan untuk produk yang paling banyak dibeli
plt.figure(figsize=(12, 6))
sns.barplot(data=df_top_products, x='product_id', y='review_score', estimator=np.mean)
plt.title('Rata-rata Ulasan Konsumen Berdasarkan Produk yang Paling Banyak Dibeli')
plt.xlabel('Product ID')
plt.ylabel('Rata-rata Ulasan')
plt.xticks(rotation=90)
st.pyplot(plt)

# Analisis Lanjutan: Tren Pembelian Bulanan
st.header("Analisis Lanjutan: Tren Pembelian Bulanan")
df_orders['order_purchase_timestamp'] = pd.to_datetime(df_orders['order_purchase_timestamp'])
df_orders.set_index('order_purchase_timestamp', inplace=True)
monthly_sales = df_orders.resample('M').size()

# Visualisasi Tren Pembelian Bulanan
plt.figure(figsize=(10, 6))
monthly_sales.plot()
plt.title('Tren Pembelian Bulanan')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Pembelian')
st.pyplot(plt)

# Kesimpulan
st.header("Kesimpulan")
st.write("**Pertanyaan 1** : Pembelian produk sangat dipengaruhi oleh kategori dan lokasi pembelian.")
st.write("**Pertanyaan 2** : Produk yang paling banyak dibeli cenderung memiliki ulasan konsumen yang lebih baik.")
st.write("**Analisis Lanjutan** : Dengan memahami pola musiman, bisnis dapat mengalokasikan sumber daya secara efisien.")

# Simpan data final ke file CSV di folder yang aman
output_path = os.path.join('dashboard', 'main_data.csv')
if not os.path.exists('dashboard'):
    os.makedirs('dashboard')
df_final.to_csv(output_path, index=False)
st.write("Data final telah disimpan di folder dashboard sebagai main_data.csv.")
