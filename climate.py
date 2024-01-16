import streamlit as st
import requests
from bs4 import BeautifulSoup
import csv
import docx
import os

# Fungsi untuk melakukan crawling website
def crawl_website(url):
    # Mengirim permintaan HTTP GET ke URL
    response = requests.get(url)

    # Memeriksa apakah permintaan berhasil
    if response.status_code == 200:
        # Membuat objek BeautifulSoup dari konten HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Menggunakan BeautifulSoup untuk mengekstrak konten yang diinginkan
        # Misalnya, mendapatkan semua teks pada halaman tersebut
        content = soup.get_text()

        # Mengembalikan konten yang ditemukan
        return content
    else:
        return None

# Fungsi untuk menyimpan hasil crawling dalam file CSV
def save_to_csv(content, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Content'])
        writer.writerow([content])

# Fungsi untuk menyimpan hasil crawling dalam file teks
def save_to_text(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

# Fungsi untuk menyimpan hasil crawling dalam file Word
def save_to_word(content, filename):
    doc = docx.Document()
    doc.add_paragraph(content)
    doc.save(filename)

# Antarmuka web menggunakan Streamlit
def main():
    st.title("Web Content Crawler")

    # Menerima input URL dari pengguna
    url = st.text_input("Masukkan URL")

    # Tombol untuk memulai crawling
    if st.button("Crawl"):
        # Memanggil fungsi crawl_website dengan URL yang diberikan
        content = crawl_website(url)

        # Menampilkan hasil crawling
        if content is not None:
            st.success("Berikut adalah konten yang ditemukan:")
            st.write(content)

            # Dropdown untuk memilih format file
            file_format = st.selectbox("Pilih format file", ["CSV", "Teks", "Word"])

            # Tombol untuk menyimpan hasil crawling dalam format file yang dipilih
            if st.button("Simpan"):
                if file_format == "CSV":
                    save_to_csv(content, 'hasil_crawling.csv')
                    st.success("Hasil crawling telah disimpan dalam file CSV.")
                elif file_format == "Teks":
                    save_to_text(content, 'hasil_crawling.txt')
                    st.success("Hasil crawling telah disimpan dalam file teks.")
                elif file_format == "Word":
                    save_to_word(content, 'hasil_crawling.docx')
                    st.success("Hasil crawling telah disimpan dalam file Word.")

                # Tautan untuk kembali ke halaman depan
                st.markdown("<a href='./'>Kembali</a>", unsafe_allow_html=True)
        else:
            st.error("Gagal melakukan crawling. Periksa URL yang Anda masukkan.")

if __name__ == "__main__":
    main()
