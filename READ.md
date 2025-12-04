# ☕ Aplikasi GUI Point of Sales (POS) — *It’s Yours Coffee*

<img src="dokumentasi/tampilan aplikasi full.jpeg" alt="Menu Preview" width="260">

Aplikasi kasir **It’s Yours Coffee** hadir untuk mendukung pengalaman transaksi yang **sederhana, cepat, dan ramah**.  
Dengan alur kerja yang terstruktur, aplikasi ini membantu kasir:

- mencatat pesanan  
- menghitung total  
- memproses pembayaran  
- menyimpan data transaksi  

Semua dirancang agar interaksi pelanggan–kasir tetap hangat tanpa mengorbankan akurasi dan kecepatan.

---

## ✨ Filosofi Nama “It’s Yours Coffee”

“It’s Yours Coffee” dipilih sebagai nama karena mencerminkan **kehangatan dan personalisasi**.  
Setiap cangkir kopi dianggap sebagai sesuatu yang:

> **“Milikmu. Dibuat spesial untukmu.”**

Nama ini memberi kesan:
- personal  
- hangat  
- inklusif  
- dekat dengan pelanggan  

---

## 🎨 Tema Warna Aplikasi

Perpaduan warna yang dipilih menghadirkan nuansa natural, tenang, dan elegan.

| Warna | Hex Code | Makna |
|-------|----------|--------|
| Putih krem lembut | `#F1F3E0` | Bersih, sederhana, ramah |
| Hijau zaitun gelap | `#778873` | Tenang, hangat, alami |
| Hijau pastel | `#D2DCB6` | Segar, seimbang, harmonis |

---

## 📑 Alur Kerja Aplikasi Kasir

Aplikasi POS ini berjalan melalui **4 tahap utama**:

---

### 1️⃣ Input Pesanan  
Kasir memilih item dari daftar menu.  
Jumlah pesanan dimasukkan melalui **spinbox/tombol + dan –**.  
Jika ada sistem poin, nomor telepon pelanggan dapat dimasukkan.

Tujuan tahap ini:  
✔ memastikan pesanan tercatat dengan **akurat & lengkap**.

---

### 2️⃣ Perhitungan  
Saat tombol **“Hitung Total”** ditekan:

- sistem menghitung subtotal (harga × jumlah)
- menambahkan **PPN 10%**
- menampilkan total bayar
- struk sementara diperbarui (item, qty, harga satuan, total per item)

Tujuan tahap ini:  
✔ memberikan perhitungan **otomatis dan minim kesalahan**.

---

### 3️⃣ Pembayaran  
Kasir memasukkan jumlah uang pelanggan.  
Sistem akan:

- memvalidasi uang cukup/tidak  
- menghitung kembalian  
- menampilkan hasil pembayaran  

Kalau uang kurang → muncul pesan error.

Tujuan tahap ini:  
✔ memastikan pembayaran **valid dan aman**.

---

### 4️⃣ Transaksi Selesai  
Sistem menampilkan:

- total pembayaran  
- uang diterima  
- kembalian  
- tanggal & waktu transaksi  

Kasir dapat menyimpan struk sebagai **file `.txt`**, lalu menekan **Reset** untuk membersihkan data dan melanjutkan ke transaksi berikutnya.

Tujuan tahap ini:  
✔ dokumentasi selesai dan aplikasi siap digunakan kembali.

---
