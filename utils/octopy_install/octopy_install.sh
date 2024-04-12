#!/bin/bash

username=$(whoami)

echo "Moving to home directory"
cd

echo "Creating App directory"
mkdir App

echo "Moving to App directory"
cd App

echo "Removing Orink_csomagolas directory"
sudo rm -r Orink_csomagolas

echo "Cloning Orink_csomagolas repository"
git clone https://github.com/notvillers/Orink_csomagolas.git

echo "Moving to home directory"
cd

echo "Removing csomagolas.sh from Desktop"
rm Desktop/csomagolas.sh

echo "Creating csomagolas.sh on Desktop"
touch Desktop/csomagolas.sh
echo "#!/bin/bash" > /Desktop/csomagolas.sh
echo "sudo bash /home/$username/App/Orink_csomagolas/start_raspi.sh" >> Desktop/csomagolas.sh

echo "Changing permissions of csomagolas.sh"
chmod +x Desktop/csomagolas.sh

echo "Creating autostart directory"
mkdir .config/autostart

echo "Removing octopy.desktop from autostart"
rm .config/autostart/octopy.desktop

echo "Creating octopy.desktop in autostart"
touch .config/autostart/octopy.desktop
echo "[Desktop Entry]" > /.config/autostart/octopy.desktop
echo "Type=Application" >> /.config/autostart/octopy.desktop
echo "Name=Octopy" >> /.config/autostart/octopy.desktop
echo "Exec=/home/$username/Desktop/csomagolas.sh" >> /.config/autostart/octopy.desktop