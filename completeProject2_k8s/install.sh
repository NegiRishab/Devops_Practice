

set -e

ENVIRONMENT=$1

# Check environment argument
if [ -z "$ENVIRONMENT" ]; then
    echo "Usage: ./install.sh <dev|stage|prod>"
    exit 1
fi

# Validate environment
case "$ENVIRONMENT" in
    dev|stage|prod)
        ;;
    *)
        echo "Invalid environment: $ENVIRONMENT"
        echo "Allowed environments: dev, staging, prod"
        exit 1
        ;;
esac

echo "=== Deploying all microservices to $ENVIRONMENT ==="

VALUES_DIR="./environments/$ENVIRONMENT"


# 1. Redis first
echo "Deploying redis..."
helm upgrade --install redis ./charts/redis \
    -f "$VALUES_DIR/redis-cart-values.yaml"


# 2. Core backend services
echo "Deploying email..."
helm upgrade --install email ./charts/microservices \
    -f "$VALUES_DIR/email-service-values.yaml"

echo "Deploying product-catalog..."
helm upgrade --install product-catalog ./charts/microservices \
    -f "$VALUES_DIR/product-catalog-service-values.yaml"

echo "Deploying payment..."
helm upgrade --install payment ./charts/microservices \
    -f "$VALUES_DIR/payment-service-values.yaml"

echo "Deploying currency..."
helm upgrade --install currency ./charts/microservices \
    -f "$VALUES_DIR/currency-service-values.yaml"

echo "Deploying shipping..."
helm upgrade --install shipping ./charts/microservices \
    -f "$VALUES_DIR/shipping-service-values.yaml"

echo "Deploying ad..."
helm upgrade --install ad ./charts/microservices \
    -f "$VALUES_DIR/ad-service-values.yaml"


# 3. Services that depend on others
echo "Deploying recommendation..."
helm upgrade --install recommendation ./charts/microservices \
    -f "$VALUES_DIR/recommendation-service-values.yaml"

echo "Deploying cart..."
helm upgrade --install cart ./charts/microservices \
    -f "$VALUES_DIR/cart-service-values.yaml"

echo "Deploying checkout..."
helm upgrade --install checkout ./charts/microservices \
    -f "$VALUES_DIR/checkout-service-values.yaml"


# 4. Frontend last
echo "Deploying frontend..."
helm upgrade --install frontend ./charts/microservices \
    -f "$VALUES_DIR/frontend-service-values.yaml"


echo "=== All services deployed successfully to $ENVIRONMENT ==="
