import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import os
from PIL import Image

# Konfigurasi Lingkungan Aplikasi
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

class AppColors:
    MAIN_BG = "#F1F3E0"
    MENU_BG = "#778873"
    MENU_CARD = "#D2DCB6"
    PAY_BG = "#778873"
    RECEIPT_BG = "#778873"
    HEADER_BG = "#D2DCB6"
    BTN_MAIN = "#778873"
    BTN_HOVER = "#452829"
    TEXT_LIGHT = "#FFFFFF"
    TEXT_DARK = "#1a1a1a"

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Modul Pendukung
def find_image_file(filename):
    """Mencoba menemukan file gambar di direktori aset. Proses ini sangat membantu memastikan visual menu termuat dengan baik."""
    if not filename: return None
    
    candidate = os.path.join(ASSETS_DIR, filename)
    if os.path.isfile(candidate): return candidate

    name_stripped = os.path.splitext(filename)[0].strip()
    exts = [".jpeg", ".jpg", ".png"]
    for ext in exts:
        p = os.path.join(ASSETS_DIR, name_stripped + ext)
        if os.path.isfile(p): return p
        
    return None

def format_rupiah(value):
    """Mengubah nilai numerik menjadi format mata uang Rupiah yang standar."""
    return f"Rp {value:,.0f}".replace(",", "_").replace(".", ",").replace("_", ".")

# Sistem Kasir Utama
class CoffeeShopApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.menu_items_data = {
            "Toffee nut": (30000, "toffee nut.jpeg"),
            "Triple Choco": (35000, "triple choco.jpeg"),
            "Matcha Red Bean": (32000, "matcha red bean.jpeg"),
            "Double Sugar": (2000, "double sugar.jpeg"),
            "Double Shoot": (3000, "double shot.jpeg"),
            "Chocolate Latte": (28000, "chocolate latte.jpeg"),
            "Matcha Latte": (30000, "matcha latte.jpeg"),
            "Black Sesam Latte": (20000, "black sesam latte.jpeg"),
        }
        self.ppn_rate = 0.10
        self.quantities = {item: ctk.StringVar(value="0") for item in self.menu_items_data}
        self.subtotal = 0.0
        self.total_price = 0.0 
        self.last_order_details = [] 

        self._initialize_ui_elements()
        self.calculate_total()

    def _initialize_ui_elements(self):
        self._initialize_fonts()
        
        self.title("☕It's Yours Coffee - Sistem Kasir")
        
        # Mengaktifkan mode layar penuh (Maximized state) setelah jeda singkat (10ms) untuk mencegah glitch rendering awal.
        def maximize_window():
            self.wm_state('zoomed')
            
        self.after(10, maximize_window)

        self.configure(fg_color=AppColors.MAIN_BG)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure((1, 2), weight=2)
        self.grid_rowconfigure(1, weight=1)

        self.menu_images = self._load_menu_images()
        self._create_header()
        self._create_menu_frame()
        self._create_payment_frame()
        self._create_receipt_frame()

    def _initialize_fonts(self):
        self.font_title_app = ctk.CTkFont(family="Arial Black", size=30, weight="bold")
        self.font_section_header = ctk.CTkFont(family="Poppins", size=22, weight="bold")
        self.font_header = ctk.CTkFont(family="Poppins", size=16)
        self.font_menu_item = ctk.CTkFont(family="Poppins", size=16, weight="bold")
        self.font_payment = ctk.CTkFont(family="Poppins", size=14)
        self.font_payment_bold = ctk.CTkFont(family="Poppins", size=14, weight="bold")
        self.font_receipt = ctk.CTkFont(family="Courier New", size=12)

    def _load_menu_images(self):
        """Memuat dan mempersiapkan gambar menu agar siap ditampilkan di kartu item."""
        images = {}
        for item, (_, img_file) in self.menu_items_data.items():
            img_full = find_image_file(img_file)
            if not img_full:
                images[item] = None
                continue
            try:
                img = Image.open(img_full).convert("RGBA")
                img_resized = img.resize((70, 70), Image.LANCZOS)
                images[item] = ctk.CTkImage(light_image=img_resized, dark_image=img_resized, size=(70, 70))
            except Exception:
                images[item] = None
        return images

    # Pembentukan Tampilan Antarmuka
    def _create_header(self):
        header = ctk.CTkFrame(self, fg_color=AppColors.HEADER_BG, corner_radius=8)
        header.grid(row=0, column=0, columnspan=3, padx=20, pady=(30, 10), sticky="ew")
        header.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(header, text="☕ Marsha Carolince's Coffee - D121231013", font=self.font_title_app, text_color=AppColors.MENU_BG).grid(row=0, column=0, padx=20, sticky="w")
        self.time_label = ctk.CTkLabel(header, text="", font=self.font_header, text_color=AppColors.TEXT_DARK)
        self.time_label.grid(row=0, column=1, padx=20, sticky="e")
        self._update_time()

    def _create_menu_frame(self):
        self.menu_frame = ctk.CTkScrollableFrame(self, label_text="📋 Daftar Menu", label_font=self.font_section_header, fg_color=AppColors.MENU_BG, label_fg_color=AppColors.MENU_BG, label_text_color=AppColors.TEXT_LIGHT, corner_radius=8, border_width=2, border_color=AppColors.MENU_CARD)
        self.menu_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.menu_frame.grid_columnconfigure(0, weight=1)

        for row, (item, (price, _)) in enumerate(self.menu_items_data.items()):
            self._create_menu_card(self.menu_frame, row, item, price)
            
    def _create_menu_card(self, parent, row, item, price):
        card = ctk.CTkFrame(parent, fg_color=AppColors.MENU_CARD, corner_radius=8)
        card.grid(row=row, column=0, padx=8, pady=6, sticky="ew")
        card.grid_columnconfigure(1, weight=1)

        img_label = ctk.CTkLabel(card, text="", fg_color=AppColors.MENU_CARD)
        if self.menu_images[item]:
            img_label.configure(image=self.menu_images[item])
        else:
            img_label.configure(text="No\nImage", text_color=AppColors.TEXT_DARK, font=self.font_header)
        img_label.grid(row=0, column=0, rowspan=2, padx=10, pady=8)

        ctk.CTkLabel(card, text=item, font=self.font_menu_item, text_color=AppColors.TEXT_DARK).grid(row=0, column=1, sticky="w", pady=(5, 0))
        ctk.CTkLabel(card, text=format_rupiah(price), font=self.font_payment, text_color=AppColors.PAY_BG).grid(row=1, column=1, sticky="w", pady=(0, 5))

        qty_frame = ctk.CTkFrame(card, fg_color=AppColors.MENU_CARD)
        qty_frame.grid(row=0, column=2, rowspan=2, padx=10)

        def increase(i=item):
            val = int(self.quantities[i].get()); self.quantities[i].set(str(val + 1)) 
            self.after(50, self.calculate_total)

        def decrease(i=item):
            val = int(self.quantities[i].get())
            if val > 0: self.quantities[i].set(str(val - 1))
            self.after(50, self.calculate_total)

        ctk.CTkButton(qty_frame, text="-", width=36, font=self.font_header, fg_color=AppColors.BTN_MAIN, hover_color=AppColors.BTN_HOVER, command=decrease).grid(row=0, column=0, padx=2)
        ctk.CTkLabel(qty_frame, textvariable=self.quantities[item], font=self.font_header, width=40, text_color=AppColors.TEXT_DARK, fg_color=AppColors.MENU_CARD).grid(row=0, column=1, padx=2)
        ctk.CTkButton(qty_frame, text="+", width=36, font=self.font_header, fg_color=AppColors.BTN_MAIN, hover_color=AppColors.BTN_HOVER, command=increase).grid(row=0, column=2, padx=2)

    def _create_row_label(self, parent_frame, title, bold=False, row_start=0):
        current_row = parent_frame.grid_size()[1]; row_index = current_row if row_start == 0 else row_start
        font = self.font_payment_bold if bold else self.font_payment
        frame = ctk.CTkFrame(parent_frame, fg_color=AppColors.PAY_BG)
        frame.grid(row=row_index, column=0, padx=20, pady=8, sticky="ew"); frame.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkLabel(frame, text=title, text_color=AppColors.TEXT_LIGHT, font=font).grid(row=0, column=0, sticky="w", padx=10)
        lbl = ctk.CTkLabel(frame, text="Rp 0", text_color=AppColors.TEXT_LIGHT, font=font)
        lbl.grid(row=0, column=1, sticky="e", padx=10)
        return lbl

    def _create_payment_frame(self):
        self.payment_frame = ctk.CTkFrame(self, fg_color=AppColors.PAY_BG, corner_radius=8)
        self.payment_frame.grid(row=1, column=1, padx=15, pady=10, sticky="nsew"); self.payment_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.payment_frame, text="💰 DETAIL PEMBAYARAN", font=self.font_section_header, text_color=AppColors.TEXT_LIGHT).grid(row=0, column=0, pady=(25, 15))

        self.total_labels_frame = ctk.CTkFrame(self.payment_frame, fg_color=AppColors.PAY_BG)
        self.total_labels_frame.grid(row=1, column=0, sticky="ew")

        self.subtotal_label = self._create_row_label(self.total_labels_frame, "Subtotal:")
        self.ppn_label = self._create_row_label(self.total_labels_frame, "PPN 10%:")
        self.total_label = self._create_row_label(self.total_labels_frame, "TOTAL:", bold=True)
        self.change_label = self._create_row_label(self.total_labels_frame, "Kembalian:", row_start=3)
        
        ctk.CTkButton(self.payment_frame, text="Hitung Total Harga", font=self.font_header, fg_color=AppColors.BTN_MAIN, hover_color=AppColors.BTN_HOVER, command=self.calculate_and_generate_receipt).grid(row=2, column=0, pady=15)

        ctk.CTkLabel(self.payment_frame, text="Uang Tunai (Rp):", text_color=AppColors.TEXT_LIGHT, font=self.font_payment).grid(row=3, column=0)
        self.cash_entry = ctk.CTkEntry(self.payment_frame, fg_color=AppColors.TEXT_LIGHT, text_color="black", width=200, font=self.font_payment)
        self.cash_entry.grid(row=4, column=0, pady=(5, 15))

        ctk.CTkButton(self.payment_frame, text="BAYAR 💳", command=self.process_payment, fg_color=AppColors.BTN_HOVER, hover_color=AppColors.BTN_MAIN, text_color=AppColors.TEXT_LIGHT, font=self.font_section_header).grid(row=5, column=0, pady=20)

        btn_frame = ctk.CTkFrame(self.payment_frame, fg_color=AppColors.PAY_BG)
        btn_frame.grid(row=6, column=0, pady=(10, 20)); btn_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(btn_frame, text="Reset 🔄", font=self.font_header, fg_color="#B91C1C", hover_color="#7F1313", command=self.reset_transaction).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Simpan Struk 💾", font=self.font_header, fg_color="#047857", hover_color="#065F46", command=self.save_receipt).grid(row=0, column=1, padx=5)

    def _create_receipt_frame(self):
        self.receipt_frame = ctk.CTkFrame(self, fg_color=AppColors.RECEIPT_BG, corner_radius=8)
        self.receipt_frame.grid(row=1, column=2, padx=15, pady=10, sticky="nsew"); self.receipt_frame.grid_columnconfigure(0, weight=1); self.receipt_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self.receipt_frame, text="📄 STRUK TRANSAKSI", font=self.font_section_header, text_color=AppColors.TEXT_LIGHT).grid(row=0, column=0, pady=(25, 15))

        self.receipt_text = ctk.CTkTextbox(self.receipt_frame, width=330, wrap="word", font=self.font_receipt, fg_color="#B4BB9F", text_color=AppColors.TEXT_LIGHT)
        self.receipt_text.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew") 
        self.receipt_text.insert("0.0", "Tekan 'Hitung Total Harga' untuk membuat struk.")

    # Logika Inti Transaksi
    def _update_time(self):
        now = datetime.now().strftime("%d-%m-%Y | %H:%M:%S")
        self.time_label.configure(text=now)
        self.after(1000, self._update_time)
        
    def calculate_total(self):
        """Secara otomatis menghitung Subtotal, PPN, dan Total Harga berdasarkan kuantitas yang dipilih. Hasil ini diperbarui real-time di panel Detail Pembayaran."""
        self.subtotal = 0; current_order = []

        for item, (price, _) in self.menu_items_data.items():
            try: qty = int(self.quantities[item].get())
            except ValueError: qty = 0

            if qty > 0:
                total = qty * price; self.subtotal += total
                current_order.append((item, qty, price, total))
                
        self.last_order_details = current_order

        if self.subtotal == 0:
            self.subtotal_label.configure(text="Rp 0"); self.ppn_label.configure(text="Rp 0")
            self.total_label.configure(text="Rp 0"); self.change_label.configure(text="Rp 0")
            self.total_price = 0.0
            return

        ppn_amount = self.subtotal * self.ppn_rate
        self.total_price = self.subtotal + ppn_amount

        self.subtotal_label.configure(text=format_rupiah(self.subtotal))
        self.ppn_label.configure(text=format_rupiah(ppn_amount))
        self.total_label.configure(text=format_rupiah(self.total_price))
        self.change_label.configure(text="Rp 0")
        
    def calculate_and_generate_receipt(self):
        """Memproses perhitungan akhir dan menghasilkan tampilan struk yang terstruktur di panel kanan."""
        self.calculate_total()
        
        if self.subtotal > 0:
            ppn_amount = self.subtotal * self.ppn_rate
            self._generate_receipt_text(self.last_order_details, self.subtotal, ppn_amount, self.total_price)
        else:
            self.receipt_text.delete("1.0", "end")
            self.receipt_text.insert("0.0", "Tekan 'Hitung Total Harga' untuk membuat struk.")
            messagebox.showwarning("Perhatian", "Pesanan masih kosong.")
            
    def _generate_receipt_text(self, details, subtotal, ppn, total):
        """Membuat output struk transaksi menggunakan alignment string untuk kerapian kolom."""
        
        WIDTH = 40
        ITEM_COL = 20
        QTY_COL = 3
        PRICE_COL = 7
        TOTAL_COL = 7
        
        current_time = datetime.now()
        tanggal = current_time.strftime("%d/%m/%Y")
        waktu = current_time.strftime("%H:%M:%S")

        header_lines = [
            "=" * WIDTH,
            "IT'S YOURS COFFEE".center(WIDTH),
            "Cookie Couture & Coffee Bar".center(WIDTH),
            "=" * WIDTH,
            f"Tanggal : {tanggal}",
            f"Waktu   : {waktu}",
            "Kasir   : Admin",
            "-" * WIDTH,
            f"{'Item'.ljust(ITEM_COL)} {'Qty'.center(QTY_COL)} {'Harga'.rjust(PRICE_COL)} {'Total'.rjust(TOTAL_COL)}",
            "-" * WIDTH
        ]
        
        item_lines = []
        for item, qty, price, total_item in details:
            price_str = format_rupiah(price)[3:]
            total_str = format_rupiah(total_item)[3:]
            
            line = f"{item.ljust(ITEM_COL)} {str(qty).center(QTY_COL)} {price_str.rjust(PRICE_COL)} {total_str.rjust(TOTAL_COL)}"
            item_lines.append(line)

        footer_lines = [
            "-" * WIDTH,
            f"{'Subtotal'.ljust(WIDTH - 10)} {format_rupiah(subtotal)[3:].rjust(10)}",
            f"{'PPN 10%'.ljust(WIDTH - 10)} {format_rupiah(ppn)[3:].rjust(10)}",
            "-" * WIDTH,
            f"{'TOTAL HARGA'.ljust(WIDTH - 10)} {format_rupiah(total)[3:].rjust(10)}",
            "\n"
        ]
        
        final_receipt = "\n".join(header_lines + item_lines + footer_lines)
        self.receipt_text.delete("1.0", "end")
        self.receipt_text.insert("1.0", final_receipt)


    def process_payment(self):
        """Memvalidasi input uang tunai, menghitung kembalian, dan mencetak detail pembayaran ke struk."""
        if self.total_price <= 0:
            messagebox.showwarning("Perhatian", "Total harga belum dihitung.")
            return

        try: cash_str = self.cash_entry.get().replace(".", "").replace(",", ""); cash = int(cash_str)
        except ValueError: messagebox.showerror("Error", "Masukkan uang tunai dalam angka yang valid."); return

        if cash < self.total_price:
            messagebox.showerror("Gagal", f"Uang tidak cukup. Kurang {format_rupiah(self.total_price - cash)}.")
            return

        change = cash - self.total_price; self.change_label.configure(text=format_rupiah(change))
        text_before = self.receipt_text.get("1.0", "end").strip()
        
        if "TOTAL HARGA" not in text_before:
            messagebox.showwarning("Perhatian", "Total harga belum dihitung. Tekan 'Hitung Total Harga' terlebih dahulu.")
            return
            
        WIDTH = 40
        payment_block = f"""
{"-" * WIDTH}
{"Uang Dibayar :".ljust(15)} {format_rupiah(cash).rjust(WIDTH - 15)}
{"Kembalian    :".ljust(15)} {format_rupiah(change).rjust(WIDTH - 15)}
{"=" * WIDTH}
{"Terima kasih telah berkunjung!".center(WIDTH)}
{"Have a great coffee time ☕💛".center(WIDTH)}
"""
        self.receipt_text.delete("end-1c", "end") 
        self.receipt_text.insert("end", payment_block)
        messagebox.showinfo("Pembayaran Berhasil", f"Pembayaran sukses! Kembalian: {format_rupiah(change)}")

    def reset_transaction(self):
        """Mereset semua kuantitas, input tunai, label harga, dan membersihkan area struk untuk memulai transaksi baru."""
        for item in self.quantities: self.quantities[item].set("0")
        self.cash_entry.delete(0, "end")
        self.subtotal_label.configure(text="Rp 0"); self.ppn_label.configure(text="Rp 0")
        self.total_label.configure(text="Rp 0"); self.change_label.configure(text="Rp 0")
        self.receipt_text.delete("1.0", "end")
        self.receipt_text.insert("0.0", "Tekan 'Hitung Total Harga' untuk membuat struk.")
        self.subtotal = 0.0; self.total_price = 0.0; self.last_order_details = []
        messagebox.showinfo("Reset", "Transaksi telah direset.")

    def save_receipt(self):
        """Menyimpan konten struk saat ini ke dalam file teks (.txt) untuk dokumentasi transaksi."""
        content = self.receipt_text.get("1.0", "end").strip()
        if "TOTAL HARGA" not in content or "Tekan 'Hitung Total Harga'" in content:
            messagebox.showwarning("Perhatian", "Belum ada transaksi selesai atau total belum dihitung.")
            return

        folder = "struk_transaksi"; os.makedirs(folder, exist_ok=True)
        filename = datetime.now().strftime("struk_it_yours_%Y%m%d_%H%M%S.txt")
        path = os.path.join(folder, filename)

        try:
            with open(path, "w", encoding="utf-8") as f: f.write(content)
            messagebox.showinfo("Berhasil", f"Struk berhasil disimpan di folder '{folder}' sebagai:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan file: {e}")


# Pengoperasian Aplikasi
if __name__ == "__main__":
    if not os.path.isdir(ASSETS_DIR):
        print(f"[PEMBERITAHUAN] Direktori 'assets' tidak ditemukan di {ASSETS_DIR}. Pastikan Anda telah membuat folder tersebut untuk memuat gambar menu.")
    
    app = CoffeeShopApp()
    app.mainloop() 