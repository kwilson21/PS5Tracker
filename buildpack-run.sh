# Instal Google Chrome
apt-get -y install libxss1 libappindicator1 libindicator7 libxi6 libgconf-2-4
apt-get -y install xorg xvfb gtk2-engines-pixbuf
apt-get -y install dbus-x11 xfonts-base xfonts-100dpi xfonts-75dpi xfonts-cyrillic xfonts-scalable

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

dpkg -i google-chrome*.deb
apt-get install -f -y

# Install Chromedriver
wget -N https://chromedriver.storage.googleapis.com/91.0.4472.101/chromedriver_linux64.zip
apt-get -y install unzip
unzip chromedriver_linux64.zip
chmod +x chromedriver

mv -f chromedriver /usr/local/share/chromedriver
ln -sf /usr/local/share/chromedriver /usr/local/bin/chromedriver
ln -sf /usr/local/share/chromedriver /usr/bin/chromedriver

chown root:root /usr/bin/chromedriver

# Clean up
rm chromedriver_linux64.zip google-chrome-stable_current_amd64.deb
