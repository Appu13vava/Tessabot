FROM python:3.10-slim

# System dependencies
RUN apt update && apt install -y git

# Set working directory
WORKDIR /app

# Copy files into container
COPY . .

# Install Python dependencies
RUN pip install -U pip && pip install -U -r requirements.txt

# Expose the port required by Koyeb
EXPOSE 8080

# Start the bot directly
CMD ["python3", "bot.py"]
