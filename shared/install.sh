#!/bin/bash
# Install with curl -sSL https://raw.githubusercontent.com/mokny/mokka/main/shared/install.sh | bash
echo "Installing Mokka"
cd ~

DIR="./mokka"
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
MOKKAPATH="$SCRIPTPATH/mokka/mokka"

echo " _____     _   _       "
echo "|     |___| |_| |_ ___ "
echo "| | | | . | '_| '_| .'|"
echo "|_|_|_|___|_,_|_,_|__,|"
echo 
echo "Website: https://github.com/mokny/mokka"
echo "Starting installation..."


if [ -d "$DIR" ]; then
    read -p "-> There is already a mokka directory. Remove? [y/N] " -r </dev/tty
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "Removing directory..."
        rm -rf ./mokka
    else
        echo "Installation aborted."
        exit 1
    fi
fi

echo "Cloning the latest nightly build..."
git clone https://github.com/mokny/mokka

echo "Setting privileges..."
cd mokka
chmod +x mokka

echo "Creating symlink to make mokka global available..."
sudo ln -sf "$MOKKAPATH" /usr/bin/mokka 

read -p "-> Do you want to edit the Configuration-File? [y/N] " -r </dev/tty
if [[ $REPLY =~ ^[Yy]$ ]]
then
    cd mokka
    cd config
    exec nano config.toml
fi

echo "Installation complete."
exit 0

