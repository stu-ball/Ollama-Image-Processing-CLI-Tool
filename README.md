
# Image Processing CLI Tool

This tool processes images from a specified directory or file using a local API for image analysis. 
It allows users to provide custom prompts and select vision-capable models for generating image descriptions.

## Features
- Encodes and processes images using a local API.
- Supports various image formats (e.g., JPG, PNG, BMP, TIFF, HEIC).
- Generates image descriptions using user-defined or default prompts.
- Logs detailed progress with categorized feedback.
- Saves results to timestamped output files.

## CLI Showcase
![image](https://github.com/user-attachments/assets/35f31676-d88a-41e6-9eae-ace8b4038756)



## Installation

1. Clone the repository:

```bash
git clone https://github.com/tristan-mcinnis/Ollama-Image-Processing-CLI-Tool.git
cd Ollama-Image-Processing-CLI-Tool
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Ensure your local API server is running at `http://localhost:11434`.

## Usage

Run the script:

```bash
python main.py
```

### Configuration

1. The default directory for images is `./data`. Create this directory and add your images before running the script.

2. Select a vision-capable model and customize the prompt during runtime.

## Supported Models

Ensure you have a vision-capable model like `llava:latest` installed on your local server.

## Output

Processed results are saved in the `./outputs` directory with timestamped filenames.

## Requirements

- Python 3.8+
- Local API server running at `http://localhost:11434`

## License

MIT License
