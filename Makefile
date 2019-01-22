
setup_minikube:
	sudo minikube delete 2>/dev/null
	sudo minikube start --vm-driver none
	sudo chown -R $$USER $$HOME/.minikube
	sudo chgrp -R $$USER $$HOME/.minikube

clean:
	kubectl delete -f https://raw.githubusercontent.com/Kong/kong-dist-kubernetes/kong-1.0/postgres.yaml
	kubectl delete -f https://raw.githubusercontent.com/Kong/kong-dist-kubernetes/kong-1.0/kong_migration_postgres.yaml
	kubectl delete -f https://raw.githubusercontent.com/Kong/kong-dist-kubernetes/kong-1.0/kong_postgres.yaml
	kubectl delete -f kong-http-config.yaml
	kubectl delete -f user.yaml
	kubectl delete -f shop.yaml
	kubectl delete -f promotion.yaml

run:
	kubectl apply -f https://raw.githubusercontent.com/Kong/kong-dist-kubernetes/kong-1.0/postgres.yaml
	kubectl apply -f https://raw.githubusercontent.com/Kong/kong-dist-kubernetes/kong-1.0/kong_migration_postgres.yaml
	kubectl apply -f https://raw.githubusercontent.com/Kong/kong-dist-kubernetes/kong-1.0/kong_postgres.yaml
	kubectl apply -f kong-http-config.yaml
	kubectl apply -f user.yaml
    kubectl apply -f shop.yaml
    kubectl apply -f promotion.yaml

build-docker-images:
	docker build -t mashape/kong-enterprise:mesh -f Dockerfile.kong-mesh .
	docker build -t mashape/kong-enterprise:mesh-http-config -f Dockerfile.kong-http-config .
	docker build -t mashape/kong-mesh-demo:user -f Dockerfile.user .
    docker build -t mashape/kong-mesh-demo:shop -f Dockerfile.shop .
    docker build -t mashape/kong-mesh-demo:promotion -f Dockerfile.promotion .
