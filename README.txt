INSTALL:

  1. Put all *.bat files into the directory which have "vim.exe".
  2. Make "online-update" directory at same place for "vim.exe"
  3. Put all *.py files into above "online-update" directory.

  This is the directory image after install.
    {VIM_INSTALL_DIR}\
      vim.exe
      UPDATE.bat
      RESTORE.bat
      online-update\
        vim-online-update.py
        updater.py
        pe32.py
        downloader.py
        extractor.py

USAGE:
  a. Double click UPDATE.bat: check and obtain update if exists.
  b. Double click RESTORE.bat: restore broken files.
