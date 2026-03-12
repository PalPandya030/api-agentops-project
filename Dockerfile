FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
EXPOSE 8501

CMD bash -c "uvicorn api_marketplace_agents.backend.main:app --host 0.0.0.0 --port 8000 & streamlit run api_marketplace_agents/dashboard/app.py --server.port 8501 --server.address 0.0.0.0"