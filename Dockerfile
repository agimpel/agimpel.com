FROM python:3.13-slim

# set python environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Create a group and user to run our app
RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser

# make and change into working directory
RUN mkdir /app
WORKDIR /app

# copy and install requirements
COPY ./requirements.txt .
RUN apt-get update && apt-get install -y build-essential python3-dev mime-support
RUN set -ex \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /app/requirements.txt

# copy all of the code files
COPY . .
RUN chmod -R 777 *
RUN chown -R appuser:appuser /app

# set up the virtual environment
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# prepare the Django server
RUN export DJANGO_KEY="default" && export DJANGO_ALLOWED_HOSTS="localhost" && export DJANGO_DEBUG=0 && python manage.py collectstatic --noinput

# expose the port for uWSGI
EXPOSE 80

# change to app user
USER appuser

# run the uwsgi server
CMD ["uwsgi", "uwsgi.ini"]