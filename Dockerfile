###################################################################
# Developed by ozymandias-cast (https://github.com/ozymandias-cast)
# License: GPLv3
###################################################################
 

#FROM ubuntu:16.04
FROM alpine:3.8

#RUN apt-get update 
#RUN apt-get install -y vlc python-pip 

RUN apk add vlc

RUN apk add gcc g++

RUN apk add make

RUN apk add python3-dev

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache


RUN pip install feedparser 
RUN pip install requests 
RUN pip install python-vlc
RUN pip install pyzmq --install-option="--zmq=bundled"

RUN mkdir /podcasts/

ADD main.py /
ADD podb.py /
ADD playlist.py /
ADD player.py /
ADD download.py /
ADD settings.py /
ADD debug_output.py /
ADD interface_s.py /

EXPOSE 4443
EXPOSE 4444
EXPOSE 4445
EXPOSE 4446
VOLUME /podcasts

CMD [ "python", "/main.py" ]


