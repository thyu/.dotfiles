"--------------------------------------------------------------
" .vimrc 
"
" Author: T.H. Yu (thyu@github)
"--------------------------------------------------------------

"--------------------------------------------------------------
" Look and feel
"--------------------------------------------------------------
set background=dark       " dark background
colorscheme elflord       " set color scheme


"--------------------------------------------------------------
" General
"--------------------------------------------------------------
set nocompatible          " turn compatibility mode off
set autoread              " auto reload when changed externally
set history=1000          " 1000 steps of history


"--------------------------------------------------------------
" Syntax
"--------------------------------------------------------------
syntax enable             " syntax based highlighting


"--------------------------------------------------------------
" Spaces and Tabs
"--------------------------------------------------------------
set tabstop=2             " tab size
set softtabstop=2         " soft tab size
set shiftwidth=4          " shiftwidth
set expandtab             " expand tab to space
filetype plugin on        " enable filetype plugin
filetype indent on        " set language based indent

" line break
set lbr                   " do not break in the middle of word
set tw=500                " width = 500
set ai                    " auto indent
set si                    " smart indent
set wrap                  " wraplines
set linebreak             " soft line break
set nolist                " soft line break

"--------------------------------------------------------------
" UI Config
"--------------------------------------------------------------
set number                " line number
set ruler                 " display current location
set showcmd               " show cmd line
set cursorline            " highlight the current line
set showmatch             " show matching parenthesis
set lazyredraw            " marco runs faster
set so=7                  " up/down margin
set mat=2                 " cursor blinking frequency

" move vertically by visual line
nnoremap j gj
nnoremap k gk

"--------------------------------------------------------------
" Search
"--------------------------------------------------------------
set incsearch             " search as characters are entered
set hlsearch              " highlight search matches
" set ignorecase          " ignore case when searching
" set smartcase           " be smart about cases when searching

"--------------------------------------------------------------
" Menu
"--------------------------------------------------------------
set wildmenu              " visual auto-complete for command


"--------------------------------------------------------------
" MISC
"--------------------------------------------------------------

" avoid rubbish characters
let $LANG='en' 
set langmenu=en
set encoding=utf8
source $VIMRUNTIME/delmenu.vim
source $VIMRUNTIME/menu.vim

" turn off annoying errorbell
set noerrorbells
set novisualbell
set t_vb=
set tm=500

" set backup
silent !mkdir ~/.vim_backup > /dev/null 2>&1
set backupdir=~/.vim_backup//
set directory=~/.vim_backup//
