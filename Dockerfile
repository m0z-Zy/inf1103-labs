FROM python:3.14

WORKDIR /app

COPY inventory_manager.py .

CMD ["python", "inventory_manager.py"] 