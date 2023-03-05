.PHONY: help
help:  ## Show definitions of all functions
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: flake
flake:  ## Apply flake8 checker in `src` folder
	flake8 src  --max-line-length=79

.PHONY: black
black:  ## Apply black checker in `src` folder
	black  --line-length 79 --check src  

.PHONY: code-check
code-check: black flake ## Run all available code checkers

.PHONY: auto-black
auto-black:  ## Run black and apply all suggestions
	black --line-length 79 src  

.PHONY: pip-install
pip-install:  ## Install all python packages using pip
	pip install -r requirements.txt

.PHONY: docker-build-push
docker-build-push:  ## Build and push docker image
	docker build -t matheusjerico/data-challenge-jobsity .
	docker push matheusjerico/data-challenge-jobsity

.PHONY: docker-compose-up
docker-compose-up:  ## Docker compose up
	docker-compose up -d

.PHONY: docker-compose-down
docker-compose-down:  ## Docker compose down
	docker-compose down
