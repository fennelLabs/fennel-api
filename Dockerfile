FROM amd64/ubuntu:latest

RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update -y && \
    ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime && \
    apt-get install -y tzdata && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    apt-get install unzip curl python3 python3-pip \
                    python3-dev libssl-dev \
                    virtualenv libpq-dev -y && \
    apt-get upgrade -y

COPY requirements.txt /opt/app/requirements.txt
RUN mkdir /opt/app/static
RUN mkdir /opt/app/mediafiles
WORKDIR /opt/app
RUN pip3 install -r requirements.txt

EXPOSE 1234

ARG FOO
ENV PYTHONUNBUFFERED=1
COPY . /opt/app

ENTRYPOINT ["./build.sh"]
