# Instal Google Chrome
sudo apt-get install libxss1 libappindicator1 libindicator7
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

sudo dpkg -i google-chrome*.deb
sudo apt-get install -f -y

# Install Chromedriver
wget -N https://chromedriver.storage.googleapis.com/91.0.4472.101/chromedriver_linux64.zip
sudo apt-get install unzip -y
unzip chromedriver_linux64.zip
chmod +x chromedriver

sudo mv -f chromedriver /usr/local/share/chromedriver
sudo ln -sf /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -sf /usr/local/share/chromedriver /usr/bin/chromedriver

# Clean up
sudo rm chromedriver_linux64.zip google-chrome-stable_current_amd64.deb