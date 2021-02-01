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
    logging.info("Configuring vim-plug")
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
        DST_PATH = VIM_PLUGIN_DIR / "vim-airline"
        f.write(f"Plug '{DST_PATH}'\n")
        shutil.copytree(SUBMODULES / "vim-airline", DST_PATH)

        # vim-airline-theme
        logging.info("Installing vim-airline-themes")
        DST_PATH = VIM_PLUGIN_DIR / "vim-airline-themes"
        f.write(f"Plug '{DST_PATH}'\n")
        f.write("let g:airline_theme='cool'\n")
        shutil.copytree(SUBMODULES / "vim-airline-themes", DST_PATH)

        # nerdtree
        logging.info("Installing NERDTree")
        DST_PATH = VIM_PLUGIN_DIR / "nerdtree"
        f.write(f"Plug '{DST_PATH}'\n")
        shutil.copytree(SUBMODULES / "nerdtree", DST_PATH)

        # goyo
        logging.info("Installing Goyo")
        DST_PATH = VIM_PLUGIN_DIR / "goyo.vim"
        f.write(f"Plug '{DST_PATH}'\n")
        shutil.copytree(SUBMODULES / "goyo.vim", DST_PATH)

        # end vim-plug
        f.write("call plug#end()\n")

def setup_tmux() -> None:
    logging.info("Copying tmux.conf")
    shutil.copy2(DOTFILES_ROOT/ "tmux.conf", Path.home() / ".tmux.conf")

if __name__ == "__main__":
    setup_vim()
    setup_tmux()
    logging.info("Setup complete!")
