# Python lite
FROM miere/python-cv


# Install software
COPY . /src/
RUN pip install -r requirements.txt
CMD gunicorn --reload -b 0.0.0.0:8080 core.app:api
