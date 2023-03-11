FROM python:3.8.8-slim
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get -y install cron
COPY ./cron.job /etc/cron.d/container_cronjob
COPY app/requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app

RUN chmod 0644 /etc/cron.d/container_cronjob
RUN crontab /etc/cron.d/container_cronjob
RUN touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log
