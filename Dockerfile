# Use alpine-python-3 image
FROM rtortori/alpine-python3

# Install prereqs
RUN apk add --no-cache gcc python3-dev openssl-dev libffi-dev musl-dev make

# Set the working directory to /
WORKDIR /

# Copy required configuration files
ADD . /

# Install requirements
RUN pip install -r requirements.txt

# Run it
CMD python /frontend.py

# Expose port 5000
EXPOSE 5000/tcp