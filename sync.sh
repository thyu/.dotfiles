#!/usr/bin/env bash

echo "+================================================+";
echo "|                 .dotfiles sync                 |";
echo "+================================================+";
echo "";

echo    ">>> This may overwrite existing files in your home directory. ";
read -p ">>> Are you sure? (y/n) " -n 1;

echo "";

if [[ $REPLY =~ ^[Yy]$ ]]; then

    BASEDIR=$(dirname "$0");

    echo ">>> Change directory...";

    cd "$BASEDIR";

    echo ">>> Pulling updates from remote...";

    git pull origin;

    echo ">>> Synchronizing files...";

    rsync --exclude ".git/" \
    --exclude ".DS_Store" \
    --exclude ".gitignore" \
    --exclude "*~" \
    --exclude "sync.sh" \
    --exclude "README.md" \
    --exclude "LICENSE" \
    -avh --no-perms . ~;

    echo ">>> Done!"

fi;
