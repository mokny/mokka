#!/usr/bin/env bash
# Install with curl -sSL https://raw.githubusercontent.com/mokny/mokka/main/shared/install.sh | bash
echo "Installing Mokka"
cd ~

DIR="~/mokka"

if [ -d "$DIR" ]; then
    read -n1 -p "There is already a mokka directory. Remove? [Y,n]" doit 
    case $doit in  
    y|Y) rm -rf ./mokka ;; 
    n|N) exit 0 ;;
    *) rm -rf ./mokka ;; 
    esac
fi

git clone https://github.com/mokny/mokka
cd mokka
chmod +x mokka