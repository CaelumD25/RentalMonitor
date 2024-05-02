# Use an official Python runtime as the base image
FROM python:3.10
RUN ln -fs /usr/share/zoneinfo/America/Los_Angeles /etc/localtime && dpkg-reconfigure -f noninteractive tzdata
WORKDIR /container
COPY . /container
RUN pip install -r requirements.txt
CMD ["python", "main.py"]