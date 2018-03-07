CONF := unicorn.conf

.PHONY: service conf clean

all: clean service

conf:
	[ ! -e /etc/apache2/sites-available/${CONF} ] && \
		sudo cp unicorn.conf /etc/apache2/sites-available/ && \
		sudo ln -s /etc/apache2/sites-available/${CONF} /etc/apache2/sites-enabled

service: conf
	sudo systemctl restart apache2

clean:
	sudo rm -rf /etc/apache2/sites-available/${CONF} \
		   		/etc/apache2/sites-enabled/${CONF}

