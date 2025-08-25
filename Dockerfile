FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

COPY . .

RUN uv pip install --system --no-cache -r src/frontend/requirements.txt
RUN uv pip install --system --no-cache .

EXPOSE 8000 8501
CMD ["sh", "-c", "uvicorn src.backend.main:app --host 0.0.0.0 --port 8000 & streamlit run src.frontend.main.py --server.port 8501 --server.address 0.0.0.0"]