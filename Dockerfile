FROM django:python2

RUN apt-get update -y && \
    apt-get upgrade -y

RUN apt-get install -y npm git && \
    ln -s /usr/bin/nodejs /usr/bin/node && \
    npm install -g bower

    		    
		    
