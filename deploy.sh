#!/bin/bash

# One-command deployment script for MKAi Goku Service
# Usage: ./deploy.sh [--region REGION] [--project PROJECT_ID]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default configuration
PROJECT_ID="mkai-agents-goku"
REGION="asia-southeast1"
SERVICE_NAME="mkai-goku"
IMAGE_NAME="backend"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  MKAi Goku Service Deployment${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --region)
            REGION="$2"
            shift 2
            ;;
        --project)
            PROJECT_ID="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [--region REGION] [--project PROJECT_ID]"
            echo "  --region    Cloud Run region (default: asia-southeast1)"
            echo "  --project   GCP project ID (default: mkai-agents-goku)"
            echo "  --help      Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Main deployment function
main() {
    print_header
    
    # Check prerequisites
    check_prerequisites
    
    # Update configuration files
    update_configuration
    
    # Deploy using Cloud Build
    deploy_with_cloud_build
    
    # Show results
    show_results
}

# Check if all prerequisites are met
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check if gcloud is installed
    if ! command -v gcloud &> /dev/null; then
        print_error "Google Cloud CLI is not installed."
        echo "Please install it from: https://cloud.google.com/sdk/docs/install"
        exit 1
    fi
    
    # Check if user is authenticated
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        print_error "You are not authenticated with Google Cloud."
        echo "Please run: gcloud auth login"
        exit 1
    fi
    
    # Check if project exists and user has access
    if ! gcloud projects describe "$PROJECT_ID" &> /dev/null; then
        print_error "Project '$PROJECT_ID' not found or you don't have access."
        echo "Please check your project ID and permissions."
        exit 1
    fi
    
    # Set the project
    gcloud config set project "$PROJECT_ID"
    print_status "Using project: $PROJECT_ID"
    
    # Enable required APIs
    print_status "Enabling required APIs..."
    gcloud services enable cloudbuild.googleapis.com --quiet
    gcloud services enable run.googleapis.com --quiet
    gcloud services enable containerregistry.googleapis.com --quiet
    
    print_status "Prerequisites check completed!"
}

# Update configuration files with current settings
update_configuration() {
    print_status "Updating configuration files..."
    
    # Update cloudbuild.yaml with current project ID
    sed -i.bak "s/_PROJECT_ID: .*/_PROJECT_ID: $PROJECT_ID/" cloudbuild.yaml
    
    # Update env-api.yaml with correct URLs
    sed -i.bak "s|API_URL: .*|API_URL: \"https://$SERVICE_NAME-$PROJECT_ID.uc.r.run.app/api/v1\"|" env-api.yaml
    
    # Update cloudbuild.yaml region if different
    sed -i.bak "s|--region', '.*'|--region', '$REGION'|" cloudbuild.yaml
    
    print_status "Configuration updated!"
}

# Deploy using Cloud Build
deploy_with_cloud_build() {
    print_status "Starting deployment with Cloud Build..."
    echo "This will:"
    echo "  1. Build Docker image as 'backend'"
    echo "  2. Push to Container Registry"
    echo "  3. Deploy to Cloud Run as 'mkai-goku'"
    echo ""
    
    # Submit build
    print_status "Submitting build to Google Cloud Build..."
    gcloud builds submit --config cloudbuild.yaml --quiet
    
    print_status "Deployment completed successfully!"
}

# Show deployment results
show_results() {
    print_status "Deployment Results:"
    echo ""
    echo "🌐 Service URLs:"
    echo "   Main:     https://$SERVICE_NAME-$PROJECT_ID.uc.r.run.app"
    echo "   API:      https://$SERVICE_NAME-$PROJECT_ID.uc.r.run.app/api/v1"
    echo "   Docs:     https://$SERVICE_NAME-$PROJECT_ID.uc.r.run.app/docs"
    echo "   Health:   https://$SERVICE_NAME-$PROJECT_ID.uc.r.run.app/health"
    echo ""
    echo "📊 Management:"
    echo "   Console:  https://console.cloud.google.com/run/detail/$REGION/$SERVICE_NAME"
    echo "   Logs:     gcloud logging read 'resource.type=cloud_run_revision AND resource.labels.service_name=$SERVICE_NAME'"
    echo ""
    echo "🔧 Useful Commands:"
    echo "   View logs:     gcloud logging tail 'resource.type=cloud_run_revision AND resource.labels.service_name=$SERVICE_NAME'"
    echo "   Check status:  gcloud run services describe $SERVICE_NAME --region=$REGION"
    echo "   Update env:    gcloud run services update $SERVICE_NAME --region=$REGION --update-env-vars KEY=VALUE"
    echo ""
    
    # Test the health endpoint
    print_status "Testing health endpoint..."
    if curl -s -f "https://$SERVICE_NAME-$PROJECT_ID.uc.r.run.app/health" > /dev/null; then
        print_status "✅ Service is healthy and responding!"
    else
        print_warning "⚠️  Service might still be starting up. Please check in a few minutes."
    fi
}

# Run main function
main "$@" 