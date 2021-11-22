FROM nginx:alpine
ARG VERSION=1
RUN echo "<h1>Version $VERSION</h1>" > /usr/share/nginx/html/index.html
