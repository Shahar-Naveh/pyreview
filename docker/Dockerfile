FROM python:3.11-slim

WORKDIR /workspace

# Install system dependencies for matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY pyproject.toml /workspace/
RUN pip install --no-cache-dir numpy matplotlib scipy jupyter jupyterlab sympy pandas

# Expose Jupyter port
EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''"]
