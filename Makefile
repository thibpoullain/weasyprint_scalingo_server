PHONY: docker-build docker-up

docker-build:
	docker build -t weasyprint-server .

docker-up:
	docker run -p 8000:5000 -e ALLOWED_ORIGINS="*" weasyprint-server
