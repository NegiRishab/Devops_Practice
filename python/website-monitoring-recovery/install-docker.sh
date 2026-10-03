#!/usr/bin/env bash
set -euo pipefail

source /etc/os-release
if [[ "$ID" != ubuntu || "$VERSION_ID" != 24.04 ]]; then
    echo 'This bootstrap targets a fresh Ubuntu 24.04 Linode.' >&2
    exit 1
fi
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y ca-certificates curl python3
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
cat > /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: ${UBUNTU_CODENAME:-$VERSION_CODENAME}
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
systemctl enable --now docker

# SSH keys remain the login method; password login is disabled after bootstrap.
printf '%s\n' 'PasswordAuthentication no' 'KbdInteractiveAuthentication no' > /etc/ssh/sshd_config.d/00-website-monitoring.conf
sshd -t
systemctl reload ssh

cd /opt/website-monitoring
docker compose config --quiet
docker compose pull
docker compose up -d
docker compose ps
