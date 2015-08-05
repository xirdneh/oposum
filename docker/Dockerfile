FROM centos:7

MAINTAINER Josue Balandrano <xirdneh@gmail.com>

EXPOSE 8000

RUN yum -y groupinstall 'Development Tools'  && \
    yum -y install epel-release && \
    yum -y install python-pip MySQL-python python-devel libjpeg-devel zlib-devel

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

WORKDIR /oPOSum/
