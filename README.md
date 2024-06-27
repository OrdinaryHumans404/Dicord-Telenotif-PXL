# Dicort-Telenotif

FROM python:3.10.11-alpine3.18

WORKDIR app/

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install --no-warn-script-location --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]

===================================================================
# GET TOKEN   "telegram_bot_token": "your_telegram_bot_token",
  Buka Telegram https://t.me/BotFather
    1 /newbot
    2 Tulis nama bot 
    3 Tulisa username bot contoh @bothasilserangan_bot
    3 nanti Kluar hasil gini
       Use this token to access the HTTP API:
        7413093419:AAEhK2mMBgYIfrSupygdsdoMDmOgv-kI2lo
    4 COPY TOken tadi Kode uniknya buat di letakan "telegram_bot_token":
    5 UNTUK     "telegram_chat_id": "your_telegram_chat_id", Sama Di isi kaya  "tgId": "your_tgId"
    
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
