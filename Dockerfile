FROM reg.aichallenge.ir/python:3.8 AS base

ENV PYTHONUNBUFFERED 1
WORKDIR /app

# Set the timezone.
RUN echo "Asia/Tehran" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update

ADD requirements.txt .
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt

FROM base AS build

ENV STATIC_ROOT /app/static
ENV MEDIA_ROOT /app/media

COPY . /app

RUN ["./manage.py", "collectstatic", "--no-input"]

RUN chmod +x ./entrypoint.sh

CMD ["./entrypoint.sh"]

FROM reg.aichallenge.ir/nginx:1.17.6 AS static

COPY --from=build /app/static /usr/share/nginx/html/static

