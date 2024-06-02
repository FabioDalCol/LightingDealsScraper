FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY install_selenium.sh install_selenium.sh

#RUN chmod +x install_selenium.sh && ./install_selenium.sh

COPY . .

CMD ["python", "main.py"]