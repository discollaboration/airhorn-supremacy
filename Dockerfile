FROM python:3.9
RUN apt update
RUN apt install -y ffmpeg
RUN pip install poetry
WORKDIR bot
COPY poetry.lock ./
COPY pyproject.toml ./
RUN poetry install
COPY . ./
CMD ["poetry", "shell", "python", "main.py"]