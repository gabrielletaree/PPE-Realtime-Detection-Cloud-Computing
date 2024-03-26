FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG UID=10002

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /app
ADD . /app

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

EXPOSE 3000

#CMD ["python", "websocket.py", "--port=3000"]
COPY . .

CMD [ "flask", "run", "--host=0.0.0.0", "--port=3000"]