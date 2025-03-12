# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG NODE_VERSION=20.12.2

################################################################################
# Use node image for base image for all stages.
FROM node:${NODE_VERSION}-alpine as build

# Set working directory for all build stages.
WORKDIR /app

# Copy package.json so that package manager commands can be used.
COPY package*.json ./
RUN npm install --force

RUN npm install -g npm@10.9.0

RUN npx ngcc --properties es2023 browser module main --first-only --create-ivy-entry-points


# Copy the rest of the source files into the image.
COPY . .

# Set build argument (default to 'development')
ARG ENVIRONMENT=production

# Set environment variable (persisting the ARG value)
ENV ENVIRONMENT=$ENVIRONMENT


RUN npm run build -- --configuration=$ENVIRONMENT




FROM nginx:stable

# copy the custom nginx configuration file to the container in the
# default location
COPY nginx.conf /etc/nginx/nginx.conf

COPY --from=build /app/dist/fuse/ /usr/share/nginx/html

EXPOSE 4200