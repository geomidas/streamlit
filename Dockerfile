FROM python:3.11
EXPOSE 8080
WORKDIR /app
COPY . ./
RUN apt update && DEBIAN_FRONTEND=noninteractive && apt install -y locales locales-all
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8
RUN pip install -r requirements.txt
ENTRYPOINT ["streamlit", "run", "perfin.py", "--server.port=8080", "--server.address=0.0.0.0"]