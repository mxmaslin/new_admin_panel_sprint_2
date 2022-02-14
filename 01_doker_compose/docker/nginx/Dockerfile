FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf && rm /var/log/nginx/*

COPY ./app/nginx/nginx.conf ./app/nginx/site.conf ./

#ENV HOME=/home/app
ENV APP_HOME=/home/app/web
#RUN mkdir -p $APP_HOME
RUN mkdir -p $APP_HOME/staticfiles
WORKDIR $APP_HOME/staticfiles
