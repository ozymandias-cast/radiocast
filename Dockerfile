FROM ubuntu:16.04
RUN apt-get update && \
    apt-get install -y vlc python-pip && \
    pip install feedparser && \
    pip install requests && \
    pip install python-vlc && \
    mkdir /podcasts/

ADD main.py /
ADD podb.py /
ADD playlist.py /
ADD player.py /
ADD download.py /
ADD settings.py /
ADD debug_output.py /

EXPOSE 4444
VOLUME /podcasts

CMD [ "python", "/main.py" ]



