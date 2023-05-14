FROM ubuntu:latest
WORKDIR /home/work

ENV TZ='America/New_York'
ENV DEBIAN_FRONTEND=noninteractive

run apt-get update && apt-get -y install python3-pip tzdata git

RUN git clone https://github.com/n-sweep/tavernbot .

RUN pip3 install .

ENTRYPOINT ["python3", "tavernbot"]

# docker run --name tavernbot --net host -dit -v /path/to/tavernbot/:/home/work/ n-sweep/twitchbot
