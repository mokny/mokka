#!/usr/bin/env bash
# Install with curl -sSL https://raw.githubusercontent.com/mokny/mokka/main/shared/install.sh | bash
cd ~
rm -rf ./mokka
git clone https://github.com/mokny/mokka
cd mokka
chmod +x mokka
chmod +x mokkad