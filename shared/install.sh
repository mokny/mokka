#!/bin/bash
# Install with curl -sSL https://raw.githubusercontent.com/mokny/mokka/main/shared/install.sh | bash
echo "Installing Mokka"
cd ~

DIR="./mokka"

echo " _____     _   _       "
echo "|     |___| |_| |_ ___ "
echo "| | | | . | '_| '_| .'|"
echo "|_|_|_|___|_,_|_,_|__,|"
echo 
echo "Website: https://github.com/mokny/mokka"
echo "Starting installation..."

if [ -d "$DIR" ]; then

    read -p "There is already a mokka directory. Remove? [Y/N] " -r </dev/tty
    echo    # (optional) move to a new line
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "Removing directory..."
        rm -rf ./mokka
    else
        echo "Installation aborted."
        exit 0
    fi

fi

echo "Cloning the latest nightly build..."
git clone https://github.com/mokny/mokka
cd mokka
chmod +x mokka