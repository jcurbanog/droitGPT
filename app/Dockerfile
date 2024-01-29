# Use the official Node.js image with the specified version as the base image
FROM node:18.13.0

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install the app dependencies
RUN npm install

# Copy the rest of the application code
COPY app/ .
COPY app/package*.json ./

# Expose the port that the app will run on (adjust if needed)
EXPOSE 4200

# Define the default command to run the Angular app
CMD ["npm", "start"]
