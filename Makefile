.PHONY: run
run:
	uvicorn --factory src.app:app_factory --reload 

.PHONY: prod
prod:
	uvicorn --factory src.app:app_factory --workers 4

.PHONY: android
android:
	uvicorn --factory src.app:app_factory --reload --host 0.0.0.0