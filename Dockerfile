
FROM python:3.6

WORKDIR /webapp
COPY . /webapp
RUN chmod -R 777 /webapp/utils
RUN /webapp/utils/remove_files.sh
RUN /webapp/utils/setup.sh
CMD /webapp/utils/start.sh