sudo apt-get update
sudo apt-get install -y clang libomp-dev build-essential
curl -sSf https://rye-up.com/get | RYE_INSTALL_OPTION="--yes" bash
source "$HOME/.rye/env"
rye sync -f