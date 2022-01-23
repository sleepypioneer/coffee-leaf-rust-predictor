TIME_STAMP := $(shell /bin/date "%Y-%m-%d_%H-%M-%S")
MODEL_NAME := coffee_leaf_rust_model_$(TIME_STAMP)

prep_data:
	python ./scripts/prep_data.py


clean_up:
	cd data/coffee-leaf-diseases/test/images && find -type f -not -path '*/other*' -not -path '*/rust*' -delete
	cd data/coffee-leaf-diseases/train/images && find -type f -not -path '*/other*' -not -path '*/rust*' -delete


train_model:
	# trains train_model
	python ./scripts/train.py --model-name $(MODEL_NAME) \
	--train-data-path ./data/coffee-leaf-diseases/train/images


convert_model:
	# converts to tflite model
	python ./scripts/convert.py --model-name $(MODEL_NAME)


move_model:
	# moves model to lambda directory
	mv ./models/$(MODEL_NAME).tflite ./src/lambda
	echo "Model moved $(MODEL_NAME)"


prep_model: train_model convert_model move_model
	echo "Model trained: $(MODEL_NAME)"


build_lamdba_function:
	cd src/lambda && \
	docker build \
		--build-arg model_name=$(MODEL_NAME).tflite \
		-t coffee-leaf-rust-model \
		.


run_lambda_server: build_lamdba_function
	docker run -p 8080:8080 coffee-leaf-rust-model


run_app:
	cd src/app && export LAMBDA_URL=http://localhost:8080/2015-03-31/functions/function/invocations ENV=dev \
	&& streamlit run --server.runOnSave=True main.py


run_app_prod:
	cd src/app && export LAMBDA_URL=https://f7avzh1qu0.execute-api.eu-central-1.amazonaws.com/default/coffee-leaf-rust-prediction \
	&& streamlit run --server.runOnSave=True main.py