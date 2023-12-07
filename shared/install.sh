#!/bin/bash
# Install with curl -sSL https://raw.githubusercontent.com/mokny/mokka/main/shared/install.sh | bash
echo "Installing Mokka"
cd ~

DIR="~/mokka"
DIR="/etc"

if [ -d "$DIR" ]; then

    read -p "There is already a mokka directory. Remove? Y/N" -n 1 -r
    echo    # (optional) move to a new line
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "Removing directory"
        rm -rf ./mokka
    else
        echo "Aborting installation!"
        exit 0
    fi

else
    echo "All ok, cloning repo"
fi

git clone https://github.com/mokny/mokka
cd mokka
chmod +x mokka