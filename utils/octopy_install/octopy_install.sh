#!/bin/bash

# variables
username=$(whoami)
app_dir="App"
octopy_dir="App/Orink_csomagolas"
csomagolas_sh="Desktop/csomagolas.sh"
git_url="https://github.com/notvillers/Orink_csomagolas.git"
autostart_dir=".config/autostart"
octopy_desktop=".config/autostart/octopy.desktop"

# script
echo "Moving to home directory"
cd

echo "Creating $app_dir directory"
mkdir "$app_dir"

echo "Removing $octopy_dir"
sudo rm -r "$octopy_dir"

echo "Cloning $git_url repository"
cd "$app_dir"
git clone "$git_url"

echo "Moving to home directory"
cd

echo "Removing $csomagolas_sh"
rm "$csomagolas_sh"

echo "Creating $csomagolas_sh"
touch "$csomagolas_sh"
echo "#!/bin/bash" > "$csomagolas_sh"
echo "sudo bash /home/$username/App/Orink_csomagolas/start_raspi.sh" >> "$csomagolas_sh"

echo "Changing permissions of $csomagolas_sh"
chmod +x "$csomagolas_sh"

echo "Creating autostart directory"
mkdir "$autostart_dir"

echo "Removing octopy.desktop from autostart"
rm "$octopy_desktop"

echo "Creating octopy.desktop in autostart"
touch "$octopy_desktop"
echo "[Desktop Entry]" > "$octopy_desktop"
echo "Type=Application" >> "$octopy_desktop"
echo "Name=Octopy" >> "$octopy_desktop"
echo "Exec=/home/$username/Desktop/csomagolas.sh" >> "$octopy_desktop"