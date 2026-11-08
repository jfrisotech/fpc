def get_makefile_content() -> str:
    """Return production-ready Makefile content with environment and build automation."""
    # Note: Makefiles require leading TAB characters (\t) for recipe commands.
    return '''.DEFAULT_GOAL := help

# Colors
CYAN  := \\033[36m
GREEN := \\033[32m
RESET := \\033[0m

.PHONY: help
help: ## Show available commands
\t@echo "$(CYAN)Available Makefile commands:$(RESET)"
\t@echo ""
\t@echo "$(GREEN)Setup & Maintenance:$(RESET)"
\t@echo "  make setup                Install dependencies (pub get)"
\t@echo "  make clean                Clean build cache and re-fetch dependencies"
\t@echo "  make upgrade              Upgrade dependencies to newest allowed versions"
\t@echo ""
\t@echo "$(GREEN)Code Generation:$(RESET)"
\t@echo "  make generate             Run build_runner once"
\t@echo "  make watch                Run build_runner in continuous watch mode"
\t@echo ""
\t@echo "$(GREEN)Quality & Tests:$(RESET)"
\t@echo "  make lint                 Run flutter analyze"
\t@echo "  make format               Format all Dart files"
\t@echo "  make test                 Run all unit and widget tests"
\t@echo "  make test-coverage        Run tests with code coverage output"
\t@echo ""
\t@echo "$(GREEN)Run Multi-Environment:$(RESET)"
\t@echo "  make run-dev              Run app with Dev environment"
\t@echo "  make run-staging          Run app with Staging environment"
\t@echo "  make run-prod             Run app with Production environment"
\t@echo ""
\t@echo "$(GREEN)Build Android (APK):$(RESET)"
\t@echo "  make build-apk-dev        Build debug APK for dev"
\t@echo "  make build-apk-staging    Build release APK for staging"
\t@echo "  make build-apk-prod       Build release APK for production"
\t@echo ""
\t@echo "$(GREEN)Build Android (AAB):$(RESET)"
\t@echo "  make build-aab-dev        Build App Bundle for dev"
\t@echo "  make build-aab-staging    Build App Bundle for staging"
\t@echo "  make build-aab-prod       Build App Bundle for production"
\t@echo ""
\t@echo "$(GREEN)Build iOS (IPA):$(RESET)"
\t@echo "  make build-ipa-dev        Build IPA for dev"
\t@echo "  make build-ipa-staging    Build IPA for staging"
\t@echo "  make build-ipa-prod       Build IPA for production"
\t@echo ""

## Setup & Maintenance
.PHONY: setup
setup:
\tflutter pub get

.PHONY: clean
clean:
\tflutter clean
\tflutter pub get

.PHONY: upgrade
upgrade:
\tflutter pub upgrade

## Code Generation
.PHONY: generate
generate:
\tdart run build_runner build --delete-conflicting-outputs

.PHONY: watch
watch:
\tdart run build_runner watch --delete-conflicting-outputs

## Quality & Tests
.PHONY: lint
lint:
\tflutter analyze

.PHONY: format
format:
\tdart format .

.PHONY: test
test:
\tflutter test

.PHONY: test-coverage
test-coverage:
\tflutter test --coverage

## Run Multi-Environment
.PHONY: run-dev
run-dev:
\tflutter run --dart-define=ENV=dev

.PHONY: run-staging
run-staging:
\tflutter run --dart-define=ENV=staging

.PHONY: run-prod
run-prod:
\tflutter run --dart-define=ENV=prod

## Build Android (APK)
.PHONY: build-apk-dev
build-apk-dev:
\tflutter build apk --debug --dart-define=ENV=dev

.PHONY: build-apk-staging
build-apk-staging:
\tflutter build apk --release --dart-define=ENV=staging

.PHONY: build-apk-prod
build-apk-prod:
\tflutter build apk --release --dart-define=ENV=prod

## Build Android (AAB)
.PHONY: build-aab-dev
build-aab-dev:
\tflutter build appbundle --dart-define=ENV=dev

.PHONY: build-aab-staging
build-aab-staging:
\tflutter build appbundle --release --dart-define=ENV=staging

.PHONY: build-aab-prod
build-aab-prod:
\tflutter build appbundle --release --dart-define=ENV=prod

## Build iOS (IPA)
.PHONY: build-ipa-dev
build-ipa-dev:
\tflutter build ipa --dart-define=ENV=dev

.PHONY: build-ipa-staging
build-ipa-staging:
\tflutter build ipa --release --dart-define=ENV=staging

.PHONY: build-ipa-prod
build-ipa-prod:
\tflutter build ipa --release --dart-define=ENV=prod
'''

