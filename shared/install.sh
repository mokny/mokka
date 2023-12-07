#!/bin/bash
# Install with curl -sSL https://raw.githubusercontent.com/mokny/mokka/main/shared/install.sh | bash
echo "Installing Mokka"
cd ~

DIR="./mokka"
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

echo " _____     _   _       "
echo "|     |___| |_| |_ ___ "
echo "| | | | . | '_| '_| .'|"
echo "|_|_|_|___|_,_|_,_|__,|"
echo 
echo "Website: https://github.com/mokny/mokka"
echo "Starting installation..."
echo "$SCRIPTPATH"

MOKKAPATH = "$SCRIPTPATH/mokka/mokka"

if [ -d "$DIR" ]; then

    read -p "There is already a mokka directory. Remove? [y/N] " -r </dev/tty
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

read -p "Make mokka command global available? (Sudo required) [y/N] " -r </dev/tty
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "sudo ln -sf $MOKKAPATH /usr/bin/mokka"
    sudo ln -sf "$MOKKAPATH" /usr/bin/mokka 
fi


echo "Installation complete."
exit 0

#