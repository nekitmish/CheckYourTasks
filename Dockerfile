FROM python:3
EXPOSE 8000

RUN git clone https://github.com/nekitmish/CheckYourTasks
RUN pip install --no-cache-dir -r /CheckYourTasks/requirements.txt