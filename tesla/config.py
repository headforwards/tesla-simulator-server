# -*- coding: utf-8 -*-
import os


class Config(object):
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = os.getenv('TESLA_PORT', 4000)
    SECRET_KEY = (
        '\xc85\x95\x9a\x80\xc1\x93\xd0\xe9\x95\x08\xfb\xbe\x85'
        '\xd0\x1aq\xd3\x95\xc9\xad \xc0\x08'
    )
    #http://docs.timdorr.apiary.io/#reference/authentication/tokens
    #TESLA_CLIENT_ID=e4a9949fcfa04068f59abb5a658f2bac0a3428e4652315490b659d5ab3f35a9e
    #TESLA_CLIENT_SECRET=c75f14bbadc8bee3a7594412c31⁄416f8300256d7668ea7e6e7f06727bfb9d220
