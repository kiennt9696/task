FROM python:3.8.0b1-slim-stretch

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt --upgrade

COPY . /usr/src/app
ENV prometheus_multiproc_dir="/tmp"
RUN chmod +x run.sh
EXPOSE 8082

#ENTRYPOINT [ "gunicorn" ]
#CMD ["-w", "2", "-b", "0.0.0.0:8082", "wsgi"]
CMD ["./run.sh"]
