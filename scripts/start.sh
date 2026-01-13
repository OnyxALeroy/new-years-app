#!/bin/bash

# Docker Compose Script for New Years App
# This script builds and starts all services: database, backend, and frontend

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting New Years App with Docker Compose...${NC}"

# Stop and remove existing containers
echo -e "${YELLOW}Stopping existing containers...${NC}"
docker-compose down

# Build and start all services
echo -e "${BLUE}Building and starting services...${NC}"
docker-compose up --build -d

# Health checks
echo -e "${YELLOW}Performing health checks...${NC}"

# Function to check service health
check_health() {
    local service=$1
    local url=$2
    local max_attempts=30
    local attempt=1
    
    echo -e "${BLUE}Checking $service health...${NC}"
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s -f -o /dev/null "$url"; then
            echo -e "${GREEN}✓ $service is healthy${NC}"
            return 0
        fi
        
        echo -e "${YELLOW}Attempt $attempt/$max_attempts: $service not ready yet...${NC}"
        sleep 2
        ((attempt++))
    done
    
    echo -e "${RED}✗ $service failed health check${NC}"
    return 1
}

# Check backend health (give it more time to start)
sleep 10
if ! check_health "backend" "http://localhost:8000/health"; then
    echo -e "${RED}Backend health check failed. Check logs with ./scripts/logs.sh backend${NC}"
    exit 1
fi

# Check frontend health  
if ! check_health "frontend" "http://localhost:3000"; then
    echo -e "${RED}Frontend health check failed. Check logs with ./scripts/logs.sh frontend${NC}"
    exit 1
fi

# Show running containers
echo -e "${BLUE}Running containers:${NC}"
docker-compose ps

echo ""
echo -e "${GREEN}All services started and healthy!${NC}"
echo -e "${GREEN}Frontend: http://localhost:3000${NC}"
echo -e "${GREEN}Backend API: http://localhost:8000${NC}"
echo -e "${GREEN}Database: mongodb://localhost:27017${NC}"
echo ""
echo -e "${BLUE}To view logs: docker-compose logs -f${NC}"
echo -e "${BLUE}To stop services: docker-compose down${NC}"