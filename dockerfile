# Use the official Python runtime image
FROM python:3.13

# Create the app directory
RUN mkdir /src

# Set the working directory inside the container
WORKDIR /src

# Set environment variables
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/src

# Upgrade pip
RUN pip install --upgrade pip

# Copy the Django project  and install dependencies
COPY requirements.txt  /src/

# run this command to install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project to the container
COPY . /src/

# Expose the Django port
EXPOSE 8000

# Run Django’s development server
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
