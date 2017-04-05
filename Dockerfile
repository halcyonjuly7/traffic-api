FROM python:3.6-alpine
ADD . /traffik
WORKDIR /traffik
RUN pip install -r requirements.txt
CMD ["python", "run.py"]