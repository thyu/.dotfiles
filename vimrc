"--------------------------------------------------------------
" .vimrc
"
" Author: T.H. Yu (thyu@github)
"--------------------------------------------------------------

"--------------------------------------------------------------
" Theme
"--------------------------------------------------------------
set background=dark 		" dark or light background
colorscheme termschool 		" the colorscheme name

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
set nospell                     " spell checking

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
set tw=0 fo=cq wm=0		" set no text wrap except re-warpping
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
" General Key Mapping
"
" < CTRL + T >          open new tab
" < CTRL + Q >          close tab
" < F2 >                Toggle paste mode
" < F3 >                Toggle spell check
"
"--------------------------------------------------------------

nnoremap j gj 			" Move vertically by visual line
nnoremap k gk			" Move vertically by visual line

noremap <C-t> :tabnew<CR>       " Ctrl-T : open new tab
noremap <C-q> :tabclose<CR>     " Ctrl-Q : close tab
inoremap <C-t> :tabnew<CR>      " Ctrl-T : open new tab
inoremap <C-q> :tabclose<CR>    " Ctrl-Q : close tab

nmap <tab> gt			" use tab to navigate tabs
nmap <s-tab> gT			" use tab to navigate tabs

set pastetoggle=<F2>		    " F2 = Paste mode
nnoremap <F3> :set spell!<CR> 	" F3 = toggle spelling check
nnoremap <F4> :NERDTree<CR>     " F4 = NERDTree
nnoremap <F5> :Goyo<CR>         " F5 = goyo

map <up> <nop>			" disable arrow keys
map <down> <nop> 		" disable arrow keys
map <left> <nop> 		" disable arrow keys
map <right> <nop> 		" disable arrow keys

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

"--------------------------------------------------------------
" Plugin setup
"--------------------------------------------------------------
runtime! plugin_config.vim


