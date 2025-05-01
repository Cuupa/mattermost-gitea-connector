#!/usr/bin/zsh

app_version=0.10

architectures=linux/amd64,linux/arm64,linux/arm/v7,linux/arm/v5,linux/arm/v6,linux/386,linux/arm64/v8,linux/ppc64le,linux/s390x

echo "Starting docker service"
systemctl start docker

echo "Setting up multi-arch build"
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
docker buildx rm builder
docker buildx create --name builder --driver docker-container --use
docker buildx inspect --bootstrap

echo "BUILDING APP IN VERSION $app_version"
docker buildx build --push --platform=$architectures -t cuupa/mattermost-gitea-connector:$app_version ./
docker buildx build --push --platform=$architectures -t cuupa/mattermost-gitea-connector:latest ./

notify-send "Build of cuupa/mattermost-gitea-connector:$app_version complete"