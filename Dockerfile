FROM python:3.11

WORKDIR /usr/src/app

COPY . /usr/src/app

EXPOSE 5432:5432

COPY requirements.txt .
RUN /usr/local/bin/python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

