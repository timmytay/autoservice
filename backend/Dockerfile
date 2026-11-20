FROM python:3.13-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY autoservice/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "-b", "0.0.0.0:8000"]