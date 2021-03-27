FROM python:3.9
RUN apt update
RUN apt install ffmpeg
RUN pip install poetry
COPY poetry.lock ./
COPY pyproject.toml ./
RUN poetry install
WORKDIR bot
COPY . ./
CMD ["python", "main.py"]