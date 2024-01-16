FROM ubuntu:22.04

WORKDIR /ETL
RUN apt-get update
RUN apt-get install -y \
    cron \
    python3.10 \
    python3-pip \
    libmysqlclient-dev
RUN apt-get install -y pkg-config
RUN apt-get install -y mysql-client
RUN apt-get install -y nano

COPY . /ETL/
RUN pip install -r requirements.txt

RUN touch /var/log/cron.log \
    && chmod 777 /var/log/cron.log
RUN crontab -l | { cat; echo "* * * * * cd /ETL && /usr/bin/python3 /ETL/getRate.py >> /var/log/cron.log 2>&1"; } | crontab -
RUN crontab -l | { cat; echo "* * * * * cd /ETL && /usr/bin/python3 /ETL/mysql_info.py >> /var/log/cron.log 2>&1"; } | crontab -


CMD cron && tail -f /var/log/cron.log

# CMD ["python3", "/ETL/getRate.py"]



