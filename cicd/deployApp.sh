#!/bin/bash

service=$(kubectl get services | grep nfl-play-gen-api)

eval $(minikube docker-env)
minikube start

if [[ -z $service ]]; then
  kubectl create -f cicd/api.yaml
else
  kubectl apply -f cicd/api.yaml
fi

sleep 30
kubectl port-forward svc/nfl-play-gen-api 5000:5000