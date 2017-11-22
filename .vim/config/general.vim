"--------------------------------------------------------------
" General
"--------------------------------------------------------------
set nocompatible                " turn compatibility mode off
set autoread                    " auto-reload on external change
set history=1000                " 1000 steps of history
set confirm                     " confirm if closing unsaved

"--------------------------------------------------------------
" Syntax
"--------------------------------------------------------------
syntax enable                   " syntax based highlighting
set nospell                       " spell checking

"--------------------------------------------------------------
" Spaces and Tabs
"--------------------------------------------------------------
set tabstop=4                   " tab size
set softtabstop=4               " soft tab size
set shiftwidth=4                " shiftwidth
set expandtab                   " expand tab to space
set backspace=indent,eol,start  " fix backspace
filetype plugin on              " enable filetype plugin
filetype indent on              " set language based indent

" line break
set lbr                         " do not break in the middle of word
set tw=500                      " width = 500
set ai                          " auto indent
set si                          " smart indent
set wrap                        " wraplines
set linebreak                   " soft line break
set nolist                      " soft line break

"--------------------------------------------------------------
" UI Config
"--------------------------------------------------------------
set number                      " line number
set ruler                       " display current location
set showcmd                     " show cmd line
set cursorline                  " highlight the current line
set showmatch                   " show matching parenthesis
set lazyredraw                  " marco runs faster
set so=7                        " up/down margin
set mat=2                       " cursor blinking frequency

"--------------------------------------------------------------
" Search
"--------------------------------------------------------------
set incsearch                   " search as characters are entered
set hlsearch                    " highlight search matches
" set ignorecase                " ignore case when searching
" set smartcase                 " be smart about cases when searching

"--------------------------------------------------------------
" Misc
"--------------------------------------------------------------
" turn off annoying errorbell
set noerrorbells
set novisualbell
set t_vb=
set tm=500
" do not use vim backup (you should use versioning stuff like git)
set nobackup
set noswapfile
" avoid rubbish characters
let $LANG='en' 
set langmenu=en
set encoding=utf8
