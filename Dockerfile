# 1. Base image use karein
FROM python:3.11-slim

# 2. Working directory set karein
WORKDIR /app

# 3. System dependencies install karein (agar Gmail API ko chahiye hon)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. requirements.txt copy aur install karein
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Sara project code copy karein
COPY . .

# 6. Hugging Face default port 7860 use karta hai
ENV PORT=7860
EXPOSE 7860

# 7. Backend ko run karne ki command
# Yahan 'main:app' ka matlab hai main.py file mein 'app' naam ka FastAPI instance hai
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]