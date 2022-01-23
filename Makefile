TIME_STAMP := $(shell /bin/date "+%Y-%m-%d_%H-%M-%S")
MODEL_NAME := coffee_leaf_rust_model_$(TIME_STAMP)


.PHONY: prep_data
prep_data:
	python ./scripts/prep_data.py

.PHONY: clean_up
clean_up:
	cd data/coffee-leaf-diseases/test/images && find -type f -not -path '*/other*' -not -path '*/rust*' -delete
	cd data/coffee-leaf-diseases/train/images && find -type f -not -path '*/other*' -not -path '*/rust*' -delete

.PHONY: train_model
train_model:
	# trains train_model
	python ./scripts/train.py --model-name $(MODEL_NAME) \
	--train-data-path ./data/coffee-leaf-diseases/train/images

.PHONY: convert_model
convert_model:
	# converts to tflite model
	python ./scripts/convert.py --model-name $(MODEL_NAME)

.PHONY: move_model
move_model:
	# moves model to lambda directory
	cp ./models/$(MODEL_NAME).tflite ./src/lambda
	cp ./models/$(MODEL_NAME).tflite ./src/flask_app
	echo "Model $(MODEL_NAME) copied to lambda and flask directories"

.PHONY: prep_model
prep_model: train_model convert_model move_model
	echo "Model trained: $(MODEL_NAME)"

.PHONY: build_lamdba_function
build_lamdba_function:
	cd src/lambda && \
	docker build \
		--build-arg model_name=$(MODEL_NAME).tflite \
		-t coffee-leaf-rust-model \
		.

.PHONY: run_lambda_server
run_lambda_server: build_lamdba_function
	docker run -p 8080:8080 coffee-leaf-rust-model

.PHONY: run_streamlit_app
run_streamlit_app:
	cd src/streamlit_app && export LAMBDA_URL=http://localhost:8080/2015-03-31/functions/function/invocations ENV=dev \
	&& streamlit run --server.runOnSave=True main.py

.PHONY: run_streamlit_app_prod
run_streamlit_app_prod:
	cd src/streamlit_app && export LAMBDA_URL=https://f7avzh1qu0.execute-api.eu-central-1.amazonaws.com/default/coffee-leaf-rust-prediction \
	&& streamlit run --server.runOnSave=True main.py


.PHONY: build_streamlit_app
build_streamlit_app:
	cd src/streamlit_app && \
	docker build \
		--build-arg lambda_url=https://f7avzh1qu0.execute-api.eu-central-1.amazonaws.com/default/coffee-leaf-rust-prediction \
		-t coffee-leaf-rust-prediction-app \
		.

.PHONY: run_streamlit_app_docker
run_streamlit_app_docker: build_streamlit_app
	docker run -p 8501:8501 coffee-leaf-rust-prediction-app
