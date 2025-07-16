# ------------------------------
# 🐳 Dockerfile
# ------------------------------
# Create a file named Dockerfile with the following content:

"""
FROM python:3.10
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

# Create requirements.txt file:
"""
fastapi
uvicorn
openai
sqlalchemy
psycopg2-binary
pydantic
python-multipart
"""

# Build and Run:
# docker build -t techrca-backend .
# docker run -d -p 8000:8000 --env-file .env techrca-backend