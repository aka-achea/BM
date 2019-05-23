# FROM python:3.7-alpine
FROM notedev:1.4

# ENV FLASK_APP web.py 
# ENV FLASK_ENV development
# ENV REFRESHED_AT 20190523

# # RUN adduser -D flasky 
# USER root 

# # WORKDIR /home/flasky 
# WORKDIR /root

# COPY fkweb/requirements.txt ./
# RUN python -m venv venv 
# RUN venv/bin/pip install -r requirements.txt 

# COPY fkweb/app app
# COPY fkweb/web.py fkweb/boot.sh fkweb/config.py fkweb/note-dev.sqlite ./


# # run-time configuration
# EXPOSE 5000
ENTRYPOINT ["./boot.sh"]