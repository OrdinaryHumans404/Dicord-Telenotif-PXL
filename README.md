# Dicort-Telenotif

# RUNING SCRIPTS
FROM python:3.10.11-alpine3.18

WORKDIR app/

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install --no-warn-script-location --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]

===================================================================
# GET Token Bot Telegram:
Buka Telegram BotFather: Kunjungi https://t.me/BotFather di aplikasi atau browser Telegram Anda.

Buat Bot Baru:
  Ketik /newbot untuk membuat bot baru.
  Berikan nama untuk bot Anda.
  BotFather akan meminta Anda memberikan username untuk bot Anda (harus diakhiri dengan "_bot", seperti @nama_bot_anda_bot).
  Dapatkan Token Bot: Setelah bot berhasil dibuat, BotFather akan memberikan pesan seperti ini:

  Copy code
  Use this token to access the HTTP API:
  7413093419:AAEhK2mMBgYIfrSupygdsdoMDmOgv-kI2lo
  Salin token ini karena Anda akan membutuhkannya untuk mengakses API bot Telegram.
  
  Langkah-Langkah Mendapatkan Chat ID Telegram:
  Buka Saluran atau Chat Telegram: Anda dapat menggunakan akun Telegram Anda atau saluran tempat Anda ingin bot mengirimkan pesan.
  
  Dapatkan Chat ID:
  
  Kirim pesan ke bot yang baru Anda buat menggunakan Telegram.
  Buka browser dan masukkan URL berikut: https://api.telegram.org/bot<TOKEN>/getUpdates, gantilah <TOKEN> dengan token bot yang telah Anda dapatkan sebelumnya.
  Cari chat dalam respons JSON untuk menemukan id yang sesuai dengan saluran atau chat yang ingin Anda gunakan sebagai tujuan pesan bot.
  Contoh Penyusunan Informasi dalam Format yang Diminta:
  json
  Copy code
  {
    "telegram_bot_token": "7413093419:AAEhK2mMBgYIfrSupygdsdoMDmOgv-kI2lo",
    "telegram_chat_id": "1234567890"
  }
  Pastikan untuk mengganti nilai "telegram_bot_token" dan "telegram_chat_id" dengan token dan chat ID yang sesuai dengan bot dan chat yang Anda buat di Telegram.

# GET Discord Webhook URL
   1 Open Discord Server: Buka server Discord di mana Anda ingin membuat webhook.

   2 Access Server Settings: Klik nama server di sudut kiri atas layar, lalu pilih "Server Settings" (Pengaturan Server).

   3 Open Integrations: Di panel kiri, klik "Integrations" (Integrasi).

   4 Create Webhook: Klik tombol "Create Webhook" (Buat Webhook).

   5 Configure Webhook: Beri nama webhook, pilih channel untuk pesan, dan atur avatar jika perlu.

   6 Copy Webhook URL: Klik "Copy Webhook URL" (Salin URL Webhook).

   7 Save Changes: Klik "Save" (Simpan).

GUNAKAN FALSE JIKA TIDAK INGIN MENGGUNAKAN SALAH SATUNYA 
   "notify_telegram": false,
   "notify_discord": true

SALAM JACKPOTTT BIG THANK FOR ALL MEMBER  [ Ghalibie ] Lounge
===================================================================
