FROM nginx

COPY ./njs /etc/nginx/njs
COPY ./cache-files/data /usr/share/nginx/html/data/
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./index.html /etc/nginx/html/index.html

EXPOSE 80