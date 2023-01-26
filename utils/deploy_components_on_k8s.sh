kubectl create -f kubernetes/deployments-list.yaml 
kubectl create -f kubernetes/config-map.yaml 
kubectl create -f kubernetes/persistent-volume.yaml 
kubectl create -f kubernetes/persistent-volume-clain.yaml 
kubectl create -k kubernetes/services.yaml