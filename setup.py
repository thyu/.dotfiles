#!/usr/bin/env python3

import shutil
import logging

from pathlib import Path

# setup logging level
logging.basicConfig(level=logging.INFO)

# some global paths
DOTFILES_ROOT = Path(__file__).resolve().parent
SUBMODULES = DOTFILES_ROOT / "submodules"

def setup_vim():

    VIMRC_PATH = Path.home() / ".vimrc"
    VIM_DIR = Path.home() / ".vim"
    VIM_PLUGIN_DIR = VIM_DIR / "vim_plugins"
    
    # remove old files / folders, copy files from .dotfiles
    logging.info(f"Remove {VIM_DIR}")
    shutil.rmtree(VIM_DIR)
    logging.info(f"Remove {VIMRC_PATH}")
    VIMRC_PATH.unlink()

    # copy default .vimrc file
    shutil.copy2(DOTFILES_ROOT/ "vimrc", VIMRC_PATH)

    # setup vim-plug plugin management
    AUTOLOAD_DIR = VIM_DIR / "autoload"
    AUTOLOAD_DIR.mkdir(parents=True, exist_ok=True)
    VIM_PLUG_SOURCE = SUBMODULES / "vim-plug/plug.vim"
    shutil.copy2(VIM_PLUG_SOURCE, AUTOLOAD_DIR)

    # install themes
    logging.info("Installing colorschemes")
    shutil.copytree(SUBMODULES / "vim-colorschemes/colors", VIM_DIR / "colors")

    # install plugins - we use a separate plugin_config.vim
    VIM_DIR.mkdir(parents=True, exist_ok=True)
    PLUGIN_CONFIG = VIM_DIR / "plugin_config.vim"
    with open(PLUGIN_CONFIG, "w") as f:

        # start vim-plug
        f.write("call plug#begin('~/.vim/vim_plugins')\n")

        # vim-airline
        logging.info("Installing vim-airline")
        f.write("Plug 'vim-airline/vim-airline'\n")
        shutil.copytree(SUBMODULES / "vim-airline", VIM_PLUGIN_DIR / "vim-airline")

        # vim-airline-theme
        logging.info("Installing vim-airline-themes")
        f.write("Plug 'vim-airline/vim-airline-themes'\n")
        f.write("let g:airline_theme='cool'\n")
        shutil.copytree(SUBMODULES / "vim-airline-themes", VIM_PLUGIN_DIR / "vim-airline-themes")

        # end vim-plug
        f.write("call plug#end()\n")

if __name__ == "__main__":
    setup_vim()
    logging.info("Setup complete!")

