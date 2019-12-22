#!/usr/bin/env python
# -*- coding: utf-8 -*-

#python -m pip install --upgrade pip
#pip3 freeze > requirements.txt
#pip3 install  -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
#pip3 uninstall -r D:\ML\StoneSpider\requirements.txt
#git config credential.helper store
#git push https://github.com/owner/repo.git
#git config --global credential.helper 'cache --timeout 7200'
#git remote set-url origin git@github.com:username/repo.git
#Echo. >test.txt
#remove ignore cache:
#git rm -r --cached .idea

import HearthstoneLanguage
import HearthstoneWindow

if __name__ == "__main__":
    language = HearthstoneLanguage.Language.English
    hslang = HearthstoneLanguage.HearthstoneLang(language)
    hsWindow = HearthstoneWindow.HearthstoneWindow(hslang)
    hsWindow.autoSearchWindow()
    hsWindow.testMove()