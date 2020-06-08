RUN:
docker-compose up

TEST:
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"data":1}' \
  http://0.0.0.0:8000/
