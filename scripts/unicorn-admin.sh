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

init_db()
{
    # cd ${UNICORN_PKG_PATH} && rm -rf migrations
    cd /tmp
    [ -e migrations ] && rm -rf migrations
    export FLASK_APP=${UNICORN_PKG_PATH}/application.py &&
        flask3 db init && \
        flask3 db migrate -m "Initialize database" && \
        flask3 db upgrade && \
        unicorn-init-admin
    rm -rf migrations
    # find ${UNICORN_PKG_PATH} -name '__pycache__' -print0 | xargs -0 rm -rf
}

reload_conf()
{
    if [ -f ~/.unicorn/unicorn.ini ] ; then
        unicorn_ini_path=~/.unicorn/unicorn.ini
    elif [ -f /etc/unicorn/unicorn.ini ] ; then
        unicorn_ini_path=/etc/unicorn/unicorn.ini
    elif [ -f ${UNICORN_PKG_PATH}/unicorn.ini ]; then
        unicorn_ini_path=${UNICORN_PKG_PATH}/unicorn.ini
    else
        echo "'unicorn.ini' is unable to locate."
        exit 1
    fi
    wsgi_user=$(`which grep` -i "\<user\>" ${unicorn_ini_path} \
        | awk -F'=' '{print $2}' | xargs)
    wsgi_group=$(`which grep` -i "\<group\>" ${unicorn_ini_path} \
        | awk -F'=' '{print $2}' | xargs)
    wsgi_threads=$(`which grep` -i "\<threads\>" ${unicorn_ini_path} \
        | awk -F'=' '{print $2}' | xargs)
    log_level=$(`which grep` -i "\<level\>" ${unicorn_ini_path} \
        | awk -F'=' '{print $2}' | xargs)
    sed -i "/WSGIDaemon/ \
        s/\(user\).*\(group\).*\(threads\).*/\1=${wsgi_user} \2=${wsgi_group} \3=${wsgi_threads}/" \
        ${DIR_SITE_AVAI}/${UNICORN_CONF}
    sed -i "/LogLevel/ \
        s/\(LogLevel\).*/\1 ${log_level}/" \
        ${DIR_SITE_AVAI}/${UNICORN_CONF}
}

run_app()
{
    PORT=${2:-5000}
    export FLASK_APP=${UNICORN_PKG_PATH}/application.py &&
        flask3 run -p ${PORT} --with-threads
}


help_msg()
{
    echo "Usage: `basename $0` <command>"
    echo
    echo "Valid command (run with root):"
    echo "  configure"
    echo "    Apply apache site configuations for UNICORN service"
    echo "  clean"
    echo "    Clean apache site configurations"
    echo "  init_db"
    echo "    Initialize database (MySQL/MariaDB) ('unicorn' database is required)"
    echo "  reload"
    echo "    Reload apache site configurations based on unicorn.ini"
    echo " run [PORT]"
    echo "    Run web application with PORT, default port is 5000"
}

EG="\033[1;32m"
fgcolor="\033[0m"

case "$1" in
    configure)
        echo -e ${EG}"Install site configuration for UNICORN..."${fgcolor}
        install_site
        echo -e ${EG}"Restart Apache service..."${fgcolor}
        restart_apache
    ;;
    clean)
        echo -e ${EG}"Clean site configuration for UNICORN..."${fgcolor}
        clean_site
        echo -e ${EG}"Restart Apache service..."${fgcolor}
        restart_apache
    ;;
    init_db)
        echo -e ${EG}"Initialize database model..."${fgcolor}
        init_db
    ;;
    reload)
        echo -e ${EG}"Reload site configuration with unicorn.ini file..."${fgcolor}
        reload_conf
        echo -e ${EG}"Restart Apache service..."${fgcolor}
        restart_apache
    ;;
    run)
        echo -e ${EG}"Running UNICORN webapp..."${fgcolor}
        run_app $@
    ;;
    *)
        help_msg
        exit 1
    ;;
esac

exit 0
