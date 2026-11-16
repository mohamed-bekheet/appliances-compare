# Running the local scrape from an Android phone (Termux)

Berty Center and El Araby refuse GitHub's servers, so they are scraped from a home/mobile connection.

1. Install **Termux from F-Droid** (the Play Store build is outdated). Allow it to run in the background (battery: unrestricted).
2. In Termux:
   ```
   pkg update -y && pkg install -y python git libxml2 libxslt clang make
   git clone https://github.com/mohamed-bekheet/appliances-compare.git
   cd appliances-compare
   git config user.name "phone"; git config user.email "phone@users.noreply.github.com"
   ```
3. Push access: create a **fine-grained personal access token** (GitHub → Settings → Developer settings), limited to this one repository with *Contents: Read and write*. Then
   ```
   git config credential.helper store
   git push   # first push asks for username + the token as password; it is then remembered
   ```
   Never paste the token in a chat.
4. Run: `bash run_phone.sh` (keep the phone charging; `termux-wake-lock` stops it sleeping).
5. Optional weekly schedule: `pkg install -y cronie termux-services`, `sv-enable crond`, then `crontab -e` and add
   `0 3 * * 5 cd ~/appliances-compare && bash run_phone.sh >> ~/scrape.log 2>&1`
   (Install the Termux:Boot add-on so cron starts after a reboot.)

If a store still answers 403 from the phone's connection, it is blocking that connection too; the scraper logs it and moves on.
