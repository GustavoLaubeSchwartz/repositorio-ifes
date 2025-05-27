FROM python:3.10

# Expose port you want your app on
EXPOSE 5174

# Upgrade pip and install requirements
COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install pydantic[email]

ENV TZ=America/Sao_Paulo
# Copy app code and set working directory
COPY . /api
WORKDIR /api/

CMD ["uvicorn", "personavix.main:app", "--reload", "--port", "5174", "--host", "0.0.0.0"]
