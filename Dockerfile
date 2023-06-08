FROM debian:stable-slim

WORKDIR /usr/src/iron

COPY sshd_config /etc/ssh/sshd_config
COPY irondome.py .
COPY read-daemon.sh .

RUN chmod +x read-daemon.sh
RUN echo "root:root" | chpasswd
RUN apt-get update && apt-get install openssh-server net-tools sysstat procps -y
RUN apt-get install vim python3 python3-pip python3-dev -y
RUN pip install --upgrade pip
RUN pip install resource psutil Observer watchdog python-daemon argparse 


CMD [ "sh", "./read-daemon.sh" ]
EXPOSE 4243
