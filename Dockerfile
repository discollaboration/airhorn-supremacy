FROM python:3.9
RUN apt update
RUN apt install -y ffmpeg
RUN pip3 install discord.py[voice] botconfig templatebot
WORKDIR bot
COPY . ./
CMD ["python", "main.py"]
