#image for updating supplemental TLEs
FROM python:3.11 as sup

WORKDIR /usr/src/app

COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "retrieve_tle_aws.py", "--mode", "sup"]

#image for updating general TLEs
FROM python:3.11 as gp

WORKDIR /usr/src/app

COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "retrieve_tle_aws.py", "--mode", "gp"]