FROM python:3
EXPOSE 8000

RUN git clone https://github.com/nit-devschool/tasks.git
RUN pip install --no-cache-dir -r /CheckYourTasks/requirements.txt