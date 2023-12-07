#!/bin/bash
# Install with curl -sSL https://raw.githubusercontent.com/mokny/mokka/main/shared/install.sh | bash
echo "Installing Mokka"
cd ~

DIR="~/mokka"
DIR="/etc"

if [ -d "$DIR" ]; then

    read -p "Are you sure? " -n 1 -r
    echo    # (optional) move to a new line
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        rm -rf ./mokka ;; 
    else
        exit 0
        # do dangerous stuff
    fi

else
    echo "All ok, cloning repo"
fi

git clone https://github.com/mokny/mokka
cd mokka
chmod +x mokka