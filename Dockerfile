
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn \
    && groupadd --system appgroup \
    && useradd --system \
       --gid appgroup \
       --create-home \
       --home-dir /home/appuser \
       appuser \
    && mkdir -p /home/appuser \
    && chown -R appuser:appgroup /home/appuser /app

COPY --chown=appuser:appgroup . .

ENV PORT=8000
ENV HOME=/home/appuser

EXPOSE 8000

USER appuser

CMD ["gunicorn", "--workers", "2", "--timeout", "120", "--bind", "0.0.0.0:8000", "app:app"]
