"--------------------------------------------------------------
" General Key Mapping
"
" < CTRL + T >          open new tab
" < CTRL + Q >          close tab
" < F2 >                Toggle paste mode
" < F3 >                Toggle spell check
" < F5 >                Reload .vimrc
"
" < F6 >                Run clang-format.py
" < F7 >                Toggle focus mode (/w Goyo)
" < F8 >                Remove trailing whitespace
" 
"--------------------------------------------------------------

" Move vertically by visual line
nnoremap j gj
nnoremap k gk

" Tab controls
noremap <C-t> :tabnew<CR>       " Ctrl-T : open new tab
noremap <C-q> :tabclose<CR>     " Ctrl-Q : close tab
inoremap <C-t> :tabnew<CR>      " Ctrl-T : open new tab
inoremap <C-q> :tabclose<CR>    " Ctrl-Q : close tab

" use tab to navigate tabs
nmap <tab> gt
nmap <s-tab> gT

" Paste mode is F2
set pastetoggle=<F2>

" toggle spelling check using F3
nnoremap <F3> :set spell!<CR>

" toggle focus mode (set in Goyo.vim)

" reload .vimrc using F5
nnoremap <silent> <F5> :so $MYVIMRC<CR>

" learn vim the hard way: disable arrow keys
map <up> <nop>
map <down> <nop>
map <left> <nop>
map <right> <nop>

" switch tabs in normal mode using tab
" (note: you might need to modify the path to clang-format)
map <F6> :pyf /usr/share/clang/clang-format.py<cr>
imap <F6> <c-o>:pyf /usr/share/clang/clang-format.py<cr>
