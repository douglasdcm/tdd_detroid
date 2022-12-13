
FROM python:3.6

WORKDIR .
COPY . .
RUN chmod -R 777 /utils
RUN ./utils/remove_files.sh
RUN ./utils/setup.sh
CMD ./utils/start.sh

EXPOSE 5000