FROM ubuntu
ADD . /traffik
WORKDIR /traffik
RUN apt-get update
RUN apt-get update postgresql-dev, gcc, python3-dev, musl-dev
RUN pip install -r requirements.txt
CMD ["python", "run.py"]