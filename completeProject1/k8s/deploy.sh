#!/usr/bin/env bash
set -euo pipefail

: "${AWS_REGION:?AWS_REGION is required}"
: "${EKS_CLUSTER_NAME:?EKS_CLUSTER_NAME is required}"
: "${BACKEND_IMAGE:?BACKEND_IMAGE is required}"
: "${FRONTEND_IMAGE:?FRONTEND_IMAGE is required}"
: "${KUBECONFIG:?Use a workspace-specific KUBECONFIG}"

mkdir -p .ci
chmod 700 .ci
aws eks update-kubeconfig --region "$AWS_REGION" --name "$EKS_CLUSTER_NAME" \
    --kubeconfig "$KUBECONFIG" --alias taskboard-ci
chmod 600 "$KUBECONFIG"

diagnostics() {
    kubectl -n taskboard get pods,pvc,svc -o wide || true
    kubectl -n taskboard get events --sort-by=.lastTimestamp || true
}
trap diagnostics ERR


envsubst '${BACKEND_IMAGE} ${FRONTEND_IMAGE}' < k8s/application.yaml > .ci/application.yaml

kubectl apply -f k8s/database.yaml
kubectl -n taskboard rollout status deployment/mongodb --timeout=10m
kubectl apply -f .ci/application.yaml
kubectl -n taskboard rollout status deployment/backend --timeout=5m
kubectl -n taskboard rollout status deployment/frontend --timeout=5m


kubectl -n taskboard exec deployment/frontend -- wget -q -O /dev/null http://127.0.0.1/api/health
kubectl -n taskboard exec deployment/frontend -- wget -q -O /dev/null http://127.0.0.1/api/tasks

kubectl -n taskboard wait service/frontend \
    --for=jsonpath='{.status.loadBalancer.ingress[0].hostname}' --timeout=10m
APP_HOST=$(kubectl -n taskboard get service frontend \
    -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
printf '\nTaskboard URL: http://%s\n' "$APP_HOST"
