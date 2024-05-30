FROM python:3.9.16

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/

RUN python -m pip install --upgrade pip

RUN pip3 install -r requirements.txt

COPY . /code/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ENTRYPOINT ["tail", "-f", "/dev/null"]

# uvicorn main:app --host 0.0.0.0 --port 8000 --reload