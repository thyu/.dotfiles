#!/usr/bin/env bash


read -p "This may overwrite existing files in your home directory. Are you sure? (y/n) " -n 1;
echo "";
if [[ $REPLY =~ ^[Yy]$ ]]; then
    BASEDIR=$(dirname "$0");
    cd "$BASEDIR";
    git pull origin;
    rsync --exclude ".git/" \
    --exclude ".DS_Store" \
    --exclude ".osx" \
    --exclude "*~" \
    --exclude "sync.sh" \
    --exclude "README.md" \
    --exclude "LICENSE" \
    -avh --no-perms . ~;
fi;
