FROM ubuntu:16.04
RUN apt-get update 
RUN apt-get install -y vlc python-pip 
RUN pip install feedparser 
RUN pip install requests 
RUN pip install python-vlc
RUN mkdir /podcasts/

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



