#!/bin/bash
#
# ENS Legis AI Clone OS - Deployment Script
# 
# This script sets up and deploys the AI Clone OS dashboard
#

set -e  # Exit on error

echo "=================================================="
echo "  ENS Legis AI Clone OS - Deployment Script"
echo "=================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    echo "Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed${NC}"
    echo "Please install Docker Compose first: https://docs.docker.com/compose/install/"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}Please edit .env file with your credentials before continuing${NC}"
    echo "Press Enter to continue once you've configured .env..."
    read
fi

# Create necessary directories
echo -e "${GREEN}Creating necessary directories...${NC}"
mkdir -p data config templates/email

# Check for credentials.json
if [ ! -f credentials.json ]; then
    echo -e "${YELLOW}Warning: credentials.json not found${NC}"
    echo "Gmail API will not work without valid credentials."
    echo "To set up Gmail API:"
    echo "  1. Go to https://console.cloud.google.com/"
    echo "  2. Create a new project"
    echo "  3. Enable Gmail API"
    echo "  4. Create OAuth 2.0 credentials"
    echo "  5. Download credentials.json to this directory"
    echo ""
    echo "Press Enter to continue without Gmail API (dashboard will still work)..."
    read
fi

# Build Docker image
echo -e "${GREEN}Building Docker image...${NC}"
docker-compose build

# Start services
echo -e "${GREEN}Starting services...${NC}"
docker-compose up -d

# Wait for services to be ready
echo -e "${GREEN}Waiting for services to start...${NC}"
sleep 5

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo -e "${GREEN}=================================================="
    echo "  Deployment Successful!"
    echo -e "==================================================${NC}"
    echo ""
    echo "Dashboard URL: http://localhost:5000"
    echo ""
    echo "Useful commands:"
    echo "  - View logs:        docker-compose logs -f dashboard"
    echo "  - Stop services:    docker-compose stop"
    echo "  - Restart services: docker-compose restart"
    echo "  - Remove all:       docker-compose down"
    echo ""
else
    echo -e "${RED}Error: Services failed to start${NC}"
    echo "Check logs with: docker-compose logs"
    exit 1
fi
