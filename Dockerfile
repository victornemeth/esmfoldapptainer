# Start from the NVIDIA CUDA base image with development tools
FROM nvidia/cuda:11.7.1-devel-ubuntu20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.8 \
    python3-pip \
    python3.8-dev \
    build-essential \
    wget \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Ensure Python3.8 is the default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1 \
    && update-alternatives --config python3

# Upgrade pip
RUN python3 -m pip install --upgrade pip

# Install PyTorch
#pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu113


# Install ESMFold with its dependencies
RUN pip install "fair-esm[esmfold]"

# Install OpenFold and remaining dependencies
RUN pip install 'dllogger @ git+https://github.com/NVIDIA/dllogger.git'
RUN pip install 'openfold @ git+https://github.com/aqlaboratory/openfold.git@4b41059694619831a7db195b7e0988fc4ff3a307'

RUN pip install modelcif biotite matplotlib

RUN pip uninstall pytorch-lightning -y
RUN pip install "pip<24.1"
RUN pip install pytorch-lightning==1.5.10

# Verify nvcc availability
RUN nvcc --version

# Set the working directory
WORKDIR /workspace

# Default command
CMD ["/bin/bash"]
