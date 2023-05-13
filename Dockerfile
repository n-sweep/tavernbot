FROM ubuntu:latest
WORKDIR /home/work

ENV TZ='America/New_York'
ENV DEBIAN_FRONTEND=noninteractive

run apt-get update && apt-get -y install python3-pip git tzdata

RUN git clone https://github.com/n-sweep/tavernbot .

RUN pip3 install .

ENTRYPOINT ["python3", "run.py"]

# docker run --name twitchbot --net host -dit -v /home/n/Documents/Python/twitchbot/:/home/work/twitchbot n-sweep/twitchbot
