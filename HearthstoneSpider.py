#!/usr/bin/env python
# -*- coding: utf-8 -*-

#pip freeze > requirements.txt
#git config credential.helper store
#git push https://github.com/owner/repo.git
#git config --global credential.helper 'cache --timeout 7200'
#git remote set-url origin git@github.com:username/repo.git

import HearthstoneLanguage
import HearthstoneWindow

if __name__ == "__main__":
    language = HearthstoneLanguage.Language.English
    hslang = HearthstoneLanguage.HearthstoneLang(language)
    hsWindow = HearthstoneWindow.HearthstoneWindow(hslang)
    hsWindow.autoSearchWindow()
    hsWindow.testMove()