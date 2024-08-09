from python:3.12.4-slim

WORKDIR /sqlite-testing

COPY requirements.txt ./requirements.txt
COPY main.py ./main.py
RUN mkdir ./db

RUN pip install -r requirements.txt 

CMD ["bash"]
