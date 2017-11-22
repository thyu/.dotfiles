#!/usr/bin/env sh

# modify this when necessary
homedir=$HOME

# setup dirs
vim_root=$homedir/.vim
vim_bundle=$vim_root/bundle
vim_autoload=$vim_root/autoload
vim_temp=$vim_root/.temp
vim_conf=$vim_root/config

# remove previous installation
rm -rf $vim_bundle/*
rm -rf $vim_autoload/*
rm -rf $vim_temp/*

# mkdir
mkdir -p $vim_root
mkdir -p $vim_bundle
mkdir -p $vim_autoload
mkdir -p $vim_temp
mkdir -p $vim_config

# pathogen
cd $vim_temp
git clone https://github.com/tpope/vim-pathogen $vim_temp/vim-pathogen
cp $vim_temp/vim-pathogen/autoload/pathogen.vim $vim_autoload
# vim colorschemes
git clone https://github.com/flazz/vim-colorschemes.git $vim_temp/vim-colorschemes
cp -r -f $vim_temp/vim-colorschemes/colors $vim_root/colors
# vim airline
git clone https://github.com/vim-airline/vim-airline $vim_bundle/vim_airline
git clone https://github.com/vim-airline/vim-airline-themes $vim_bundle/vim_airline-themes
# nerd tree
git clone https://github.com/scrooloose/nerdtree.git $vim_bundle/nerdtree
vim -u NONE -c "helptags $vim_bundle/nerdtree/doc" -c q
# fugitive
git clone https://github.com/tpope/vim-fugitive.git $vim_bundle/vim-fugitive
vim -u NONE -c "helptags $vim_bundle/vim-fugitive/doc" -c q
# indent
git clone https://github.com/nathanaelkane/vim-indent-guides.git $vim_bundle/vim-indent-guides
# c++ highlight
git clone https://github.com/octol/vim-cpp-enhanced-highlight.git $vim_bundle/syntax/
# ctrlp
git clone https://github.com/ctrlpvim/ctrlp.vim.git $vim_bundle/ctrlp.vim
# goyo focus mode /w limelight
git clone https://github.com/junegunn/goyo.vim $vim_bundle/goyo
git clone https://github.com/junegunn/limelight.vim $vim_bundle/limelight.vim
# trailing-whitespace
git clone https://github.com/bronson/vim-trailing-whitespace $vim_bundle/vim-trailing-whitespace

# clean up temp folder
rm -rf $vim_temp
