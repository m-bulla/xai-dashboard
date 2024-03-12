FROM python:3.8-slim

WORKDIR /app
COPY . /app

#install all libraries for app
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

# update; 8050 is standard port for Dash
EXPOSE 8050

#Go to folder where .streamlit folder is
WORKDIR /app/src
CMD ["python", "main.py"]
