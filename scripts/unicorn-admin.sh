#!/bin/bash

#
# Administration script for UNICORN service.
#
#

set -e

DIR_SITE_AVAI=/etc/apache2/sites-available
UNICORN_CONF=unicorn.conf
UNICORN_PKG_PATH=/usr/share/unicorn

is_apache_installed()
{
    if [ -e ${DIR_SITE_AVAI} ] ; then
        return 0
    fi
    return 1
}

copy_conf_files()
{
    [ ! -e /var/log/unicorn ] && mkdir /var/log/unicorn
    cp ${UNICORN_PKG_PATH}/${UNICORN_CONF} ${DIR_SITE_AVAI} && \
        ln -s ${DIR_SITE_AVAI}/${UNICORN_CONF} ${DIR_SITE_AVAI}/../sites-enabled
}

restart_apache()
{
    systemctl restart apache2
}

install_site()
{
    if is_apache_installed ; then
        if ! [ -e ${DIR_SITE_AVAI}/${UNICORN_CONF} ] ; then
            copy_conf_files
        fi
    else
        echo "apache is not installed..."
        exit 1
    fi
}

clean_site()
{
    rm -rf ${DIR_SITE_AVAI}/${UNICORN_CONF} \
           ${DIR_SITE_AVAI}/../sites-enabled/${UNICORN_CONF} \
           /var/log/unicorn 2>/dev/null
}

help_msg()
{
    echo "Usage: `basename $0` <command>"
    echo
    echo "Valid command (run with root):"
    echo "  configure"
    echo "    Apply apache site configuation for UNICORN service"
    echo "  clean"
    echo "    Clean configurations"
}

case "$1" in
    configure)
        install_site
        restart_apache
    ;;
    clean)
        clean_site
        restart_apache
    ;;
    *)
        help_msg
        exit 1
    ;;
esac

exit 0
