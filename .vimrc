"--------------------------------------------------------------
" .vimrc
"
" Author: T.H. Yu (thyu@github)
"--------------------------------------------------------------
" Load pathogen
execute pathogen#infect()
syntax on
filetype plugin indent on

runtime! config/general.vim
runtime! config/mapping.vim
runtime! config/look_and_feel.vim
runtime! config/plugin/*.vim
