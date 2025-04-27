# Langkah Kerja UTS

1. Download terlebih dahulu framework yang ingin digunakan (untuk kasus ini menggunakan Python Django dan SQL)
    - pip install django
    - pip install mysqlclient
3. Buat project pada Django menggunakan command django-admin startproject nama projek
4. Buat aplikasi dengan menggunakan command django-admin startapp nama_app
5. Kemudian setting Database untuk Django pada folder projek di settings.py
   DATABASES [
     ....
   ]
7. Setelah itu masukkan app yang kita buat ke installed app.
  INSTALLED_APPS [
    ....
    app_kita
  ]
8. Setelah itu buat Model Database yaitu Admin, Kategori, Supplier, dan Item
9. Kemudian add config pada settings.py untuk custom admin
10. Kemudian lakukan migrasi dengan python manage.py makemigrations dan python manage.py migrate
11. Buat superuser untuk melakukan testing dan debug jika masih kesulitan menggunakan custom user
    python manage.py createsuperuser
    Username: Admin
    Password: Admin
    Jika ada prompt yang memberi tahu bahwa Username dan Password terlalu mirip, dapat di Bypass

12. Buat Admin Panel di folder app/admin.py
13. Kemudian buat views untuk aplikasi backend pada app/views.py
      views berisi web untuk read write data, laporan data, serta fungsi lainnya seperti memunculkan barang dengan stok rendah
15. Kemudian set url untuk app pada app/urls.py (tidak ada file urls.py pada folder app sehingga harus membuat sendiri)
16. Tambahkan url pada urls.py yang terletak pada folder projek
17. Kemudian lakukan kontainerisasi projek dengan docker dengan menggunakan file docker-compose.yml dan juga buat file Dockerfile
18. buat file requirement.txt dan isi sesuai dengan library yang kita pakai pada saat membuat projek Django (Django, mysqlclient)
19. Build aplikasi dengan command docker-compose up --build dan lakukan testing pada url localhost:8000/admin
