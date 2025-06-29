FROM python:3.11-slim
WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY ./main.py /app/
COPY ./seed.py /app/

COPY ./data /app/data

EXPOSE 8000
CMD ["sh", "-c", "python seed.py && uvicorn main:app --host 0.0.0.0 --port 8000"]
