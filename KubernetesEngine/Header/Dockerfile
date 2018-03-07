FROM gcr.io/google-appengine/python
COPY . /app
WORKDIR /app
RUN pip install -r /app/requirements.txt
CMD ["python", "run.py"]
