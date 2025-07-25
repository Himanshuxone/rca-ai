# Makefile for TechRCA Frontend

install:
	@echo "🔧 Installing frontend dependencies..."
	npm install

start:
	@echo "🚀 Starting the React frontend..."
	npm start

build:
	@echo "📦 Building production files..."
	npm run build

clean:
	@echo "🧹 Removing node_modules and build..."
	rm -rf node_modules/ build/

reinstall: clean install

help:
	@echo "Usage:"
	@echo "  make install     - Install npm dependencies"
	@echo "  make start       - Start the frontend in dev mode"
	@echo "  make build       - Build for production"
	@echo "  make clean       - Delete node_modules and build"
	@echo "  make reinstall   - Clean and install again"
