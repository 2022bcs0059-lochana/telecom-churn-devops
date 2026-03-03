FROM python:3.12

WORKDIR /app

# Copy everything into container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run ML version
CMD ["uvicorn", "app.main_ml:app", "--host", "0.0.0.0", "--port", "8000"]
