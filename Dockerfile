FROM python:3.12-slim

WORKDIR /app

COPY tele/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY tele/ ./tele/

CMD ["python", "-m" , "bot.py"]