

set -e

echo "=== Uninstalling all microservices ==="

echo "Uninstalling frontend..."
helm uninstall frontend

echo "Uninstalling checkout..."
helm uninstall checkout

echo "Uninstalling cart..."
helm uninstall cart

echo "Uninstalling recommendation..."
helm uninstall recommendation

echo "Uninstalling ad..."
helm uninstall ad

echo "Uninstalling shipping..."
helm uninstall shipping

echo "Uninstalling currency..."
helm uninstall currency

echo "Uninstalling payment..."
helm uninstall payment

echo "Uninstalling product-catalog..."
helm uninstall product-catalog

echo "Uninstalling email..."
helm uninstall email

echo "Uninstalling redis..."
helm uninstall redis

echo "=== All services uninstalled successfully ==="
