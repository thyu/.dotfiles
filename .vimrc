"--------------------------------------------------------------
" .vimrc 
"
" Author: T.H. Yu (thyu@github)
"--------------------------------------------------------------

"--------------------------------------------------------------
" Look and feel
"--------------------------------------------------------------
set background=dark             " dark background
colorscheme lucius              " set color scheme

" vim-airline
set laststatus=2                " necessary for showing airline
let g:airline_theme='molokai'   " airline theme
let g:airline#extensions#tabline#enabled=1 "enable tabline 

"--------------------------------------------------------------
" General
"--------------------------------------------------------------
set nocompatible                " turn compatibility mode off
set autoread                    " auto-reload on external change
set history=1000                " 1000 steps of history
set confirm                     " confirm if closing unsaved

" Load pathogen
execute pathogen#infect() 


"--------------------------------------------------------------
" Syntax
"--------------------------------------------------------------
syntax enable                   " syntax based highlighting


"--------------------------------------------------------------
" Spaces and Tabs
"--------------------------------------------------------------
set tabstop=2             " tab size
set softtabstop=2         " soft tab size
set shiftwidth=2          " shiftwidth
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

"--------------------------------------------------------------
" Key Mapping
"--------------------------------------------------------------

" Move vertically by visual line
nnoremap j gj
nnoremap k gk

noremap <C-t> :tabnew<CR>       " Ctrl-T : open new tab
noremap <C-w> :tabclose<CR>     " Ctrl-W : close tab
inoremap <C-t> :tabnew<CR>      " Ctrl-T : open new tab
inoremap <C-w> :tabclose<CR>    " Ctrl-W : close tab

noremap <C-n> :NERDTreeTabsToggle<CR>   " Ctrl-N Toggle NERD tree

map <C-K> :pyf ~/.scripts/clang-format.py<cr>
imap <C-K> <c-o>:pyf ~/.scripts/clang-format.py<cr>

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
