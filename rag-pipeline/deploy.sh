#!/bin/bash
if [ "$1" = "k8s" ]; then
  kubectl apply -f k8s/
  echo "☸️ Kubernetes deployment started for Rabeel-Ashraf!"
else
  docker-compose up --build
fi
