#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app as application


if __name__ == '__main__':
    application.run(threaded=True)
    #application.run()
