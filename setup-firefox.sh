add-apt-repository ppa:mozillateam/firefox-next
apt -y install firefox

wget https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz
tar xzf geckodriver-v0.29.1-linux64.tar.gz
chmod +x geckodriver
mv geckodriver /usr/bin/geckodriver
rm geckodriver-v0.29.1-linux64.tar.gz
