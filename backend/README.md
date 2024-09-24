# Backend Setup for Project
The backend of this project is built using **Flask**, a lightweight and powerful web framework for Python. This document will guide you through setting up the backend and ensuring that everything is correctly configured.

## Prerequisites

Before setting up the backend, make sure you have the following installed and configured on your machine:

- **CUDA Toolkit**
- **Ollama** (for running models)

### Step 1: Download CUDA Toolkit

Go to the following link and download the CUDA driver and toolkit: [CUDA Toolkit 11.8 Downloads](https://developer.nvidia.com/cuda-11-8-0-download-archive). 

After installation, verify that CUDA has been installed correctly by running the following command in the Command Prompt:

```bash
nvidia-smi
```
### Step 2: Download Ollama
Download and install Ollama from this link: [Ollama for windows](https://ollama.com/download/OllamaSetup.exe).

###  Step 3: Set Environmental Variables for Ollama
You will need to configure environment variables to work with Ollama. Follow these steps:

    1 Open the Environment Variables settings on your system.

    2 Set the following user variables:

-   OLLAMA_HOST: Set this to any available port number, for example, localhost:5000.
-   CUDA_VISIBLE_DEVICES: Set this based on how many GPUs are available on your machine.
    -   If you have 1 GPU, set it to 0.
    -   If you have 2 GPUs, set it to 0,1, and so on.
-   OLLAMA_MODELS: Set this to the folder where you want to download your models. Ensure that this directory has sufficient storage space.

### Step 4: Pull the Model
Once Ollama is set up, pull the necessary model using the following command in Command Prompt:
```bash
ollama pull llava
```
This command will download the required model for running the backend.

## Setting up the Backend Code
To set up the backend for running your project, follow these steps
### 1. Download and Update the `.pt` Paths in `data.yaml`
Model checkpoints can be found at: [Models](https://mega.nz/folder/1AJUlCjJ#xe-cSYsXYUftdpdZo_AzRw).

Download the required model checkpoints and update the paths in `data.yaml` to point to the downloaded checkpoints.

### 2. Download the Dependencies
The backend Folder has 2 more folders **Tass** and **timeline_backend** and each of these have have a `requirement.txt` file download them using this command 
```bash
pip install -r Tass/requirements.txt
pip install -r timeline_backend/requirements.txt
```

### 3. Run the `server.py` Script
Navigate to the `model_pipeline` directory within **TASS** directory and run the `server.py` script using any available port. You can specify the port like this:
```bash
python server.py --port 5000
```
This will start the backend server and listen for incoming requests.

## Debugging and Additional Information
-   If you encounter any issues during setup, ensure that all paths are correctly set in the `data.yaml` file.
-   Ensure that your environmental variables, especially `OLLAMA_HOST`, `CUDA_VISIBLE_DEVICES`, and `OLLAMA_MODELS`, are correctly configured.
-   For further assistance with CUDA or Ollama, refer to their official documentation
    -   [CUDA documentation](https://docs.nvidia.com/cuda/index.html)
    -   [Ollama](https://github.com/ollama/ollama)
