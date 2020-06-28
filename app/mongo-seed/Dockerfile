FROM mongo

COPY init.json /init.json
CMD mongoimport --host mongodb --db yousician --collection songs --type json --file /init.json
