#!/bin/bash

username=$(whoami)

cd
mkdir App
cd App
rm -r Orink_csomagolas
git clone https://github.com/notvillers/Orink_csomagolas.git
cd
rm /Desktop/csomagolas.sh
echo "#!/bin/bash" > /Desktop/csomagolas.sh
echo "sudo bash /home/$username/App/Orink_csomagolas/start_raspi.sh" >> /Desktop/csomagolas.sh
chmod +x /Desktop/csomagolas.sh
mkdir /.config/autostart
rm /.config/autostart/octopy.desktop
echo "[Desktop Entry]" > /.config/autostart/octopy.desktop
echo "Type=Application" >> /.config/autostart/octopy.desktop
echo "Name=Octopy" >> /.config/autostart/octopy.desktop
echo "Exec=/home/$username/Desktop/csomagolas.sh" >> /.config/autostart/octopy.desktop