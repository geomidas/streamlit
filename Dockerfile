FROM python:3.11slim
EXPOSE 8501
COPY . ./
RUN apt update && DEBIAN_FRONTEND=noninteractive && apt install -y locales locales-all
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8
RUN python -m ensurepip --upgrade
RUN pip3 install -r requirements.txt
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENTRYPOINT [ "streamlit", "run", "perfin.py"]
