
echo "=== Deploying all microservices ==="

# 1. Redis first (cart depends on it)
echo "Deploying redis..."
helm install redis ./charts/redis -f values/redis-cart-values.yaml

# 2. Core backend services (no cross-deps)
echo "Deploying email..."
helm install email ./charts/microservices -f values/email-service-values.yaml

echo "Deploying product-catalog..."
helm install product-catalog ./charts/microservices -f values/product-catalog-service-values.yaml

echo "Deploying payment..."
helm install payment ./charts/microservices -f values/payment-service-values.yaml

echo "Deploying currency..."
helm install currency ./charts/microservices -f values/currency-service-values.yaml

echo "Deploying shipping..."
helm install shipping ./charts/microservices -f values/shipping-service-values.yaml

echo "Deploying ad..."
helm install ad ./charts/microservices -f values/ad-service-values.yaml

# 3. Services that depend on others
echo "Deploying recommendation..."
helm install recommendation ./charts/microservices -f values/recommendation-service-values.yaml

# TODO: add cart-service-values.yaml — checkout & frontend need cart-service:12000
echo "Deploying cart..."
helm install cart ./charts/microservices -f values/cart-service-values.yaml

echo "Deploying checkout..."
helm install checkout ./charts/microservices -f values/checkout-service-values.yaml

# 4. Frontend last (depends on almost everything)
echo "Deploying frontend..."
helm install frontend ./charts/microservices -f values/frontend-service-values.yaml

echo "=== All services deployed ==="