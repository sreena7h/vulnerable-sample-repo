# Use official Python image with the required version
FROM python:3.12.8

# Set the working directory inside the container
WORKDIR /app

# Copy all files from the current directory (inside vulnerable-sample-repo)
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port if needed (optional)
EXPOSE 5000

# Set the entrypoint to run the application
CMD ["python", "app.py"]
