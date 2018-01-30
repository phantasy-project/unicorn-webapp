#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app as application


if __name__ == '__main__':
    #application.run(host="0.0.0.0", debug=True)
    application.run(host="0.0.0.0",
                    #ssl_context='adhoc',
                    ssl_context=("cert.pem", "key.pem"),
                    threaded=True,
                    debug=True)
