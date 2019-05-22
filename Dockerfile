FROM python:3.7-alpine

ENV FLASK_APP web.py 
ENV FLASK_ENV=development
ENV FLASK_CONFIG docker 

RUN adduser -D flasky 
USER flasky 

WORKDIR /home/flasky 

COPY fkweb fkweb
# RUN python -m venv venv 
# RUN venv/bin/pip install -r fkweb/requirements.txt 
RUN pip install -r fkweb/requirements.txt 



# run-time configuration
EXPOSE 5000
ENTRYPOINT ["fkweb/boot.sh"]