import base64
import json
import requests
import os
from PIL import Image
import io
from rich.console import Console
from rich.logging import RichHandler
import logging
from typing import List
from datetime import datetime

# Constants
SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff', '.tif', '.heic', '.heif')
DEFAULT_PROMPT = "Describe this image, highlighting any notable details (including visible text):"

# Set up Rich console and logging
console = Console()
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console, rich_tracebacks=True)]
)
log = logging.getLogger("rich")

# Helper: Log categories
def log_message(category: str, message: str) -> None:
    icons = {
        "start": "🚀",
        "progress": "🔄",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌",
        "completion": "🎉"
    }
    icon = icons.get(category, "")
    log.info(f"{icon} {message}")

# Encode image
def encode_image(image_path: str) -> str:
    try:
        with Image.open(image_path) as img:
            img.thumbnail((800, 800))
            img = img.convert('RGB')
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG")
            return base64.b64encode(buffer.getvalue()).decode('utf-8')
    except Exception as e:
        log_message("error", f"Failed to encode image: {e}")
        raise

# Generate image description
def generate_image_description(image_path: str, prompt: str, model: str) -> str:
    base64_image = encode_image(image_path)
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "images": [base64_image]
    })
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post("http://localhost:11434/api/generate", headers=headers, data=payload)
        if response.status_code == 400:
            log_message("error", f"Model {model} doesn't support image analysis. Please use a vision-capable model.")
            return "Error: Model doesn't support image analysis"
        response.raise_for_status()
        return response.json().get('response', "No response provided by API")
    except requests.exceptions.RequestException as e:
        log_message("error", f"API call failed: {e}")
        raise

# Process images
def ensure_directory_exists(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)
        log_message("warning", f"Created directory: {directory}")

def write_header(f, model: str, prompt: str) -> None:
    f.write(f"Image Analysis Results\n")
    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Model: {model}\n")
    f.write(f"Prompt: {prompt}\n")
    f.write("-" * 80 + "\n\n")

def write_result(f, index: int, filename: str, description: str) -> None:
    f.write(f"Image {index}: {filename}\n")
    f.write(f"{description}\n")
    f.write("-" * 80 + "\n\n")

def process_images(path: str, prompt: str, model: str) -> None:
    outputs_dir = "./outputs"
    ensure_directory_exists(outputs_dir)

    if os.path.isfile(path):
        image_files = [path] if path.lower().endswith(SUPPORTED_EXTENSIONS) else []
    elif os.path.isdir(path):
        image_files = [os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith(SUPPORTED_EXTENSIONS)]
    else:
        log_message("error", f"Invalid path: {path}")
        return

    total_images = len(image_files)
    log_message("start", f"Found {total_images} images to process.")
    if total_images == 0:
        log_message("warning", "No valid images found. Exiting.")
        return

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_file = os.path.join(outputs_dir, f"{timestamp}.txt")

    with open(output_file, 'w', encoding='utf-8') as f:
        write_header(f, model, prompt)
        for index, filepath in enumerate(image_files, start=1):
            try:
                filename = os.path.basename(filepath)
                log_message("progress", f"Processing image {index}/{total_images}: {filename}")
                description = generate_image_description(filepath, prompt, model)
                log_message("success", f"Description for {filename}:")
                log.info(f"[yellow]{description}[/yellow]")
                write_result(f, index, filename, description)
            except Exception as e:
                error_msg = f"Error processing {filepath}: {e}"
                log_message("error", error_msg)
                failed_filename = os.path.basename(filepath)
                write_result(f, index, failed_filename, f"Error processing {failed_filename}: {str(e)}")

    log_message("completion", f"Results saved to {output_file}")
    log_message("completion", "Image processing completed successfully!")

def get_available_models() -> List[str]:
    """Fetch available vision-capable models from Ollama"""
    vision_models = [
        "llava", "llava-phi3", "llama3.2-vision",
        "bakllava", "cogvlm", "qwen-vl",
        "gemma3:4b", "gemma3"
    ]
    try:
        response = requests.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        all_models = [model['name'] for model in response.json().get('models', [])]
        available_vision_models = [
            model for model in all_models
            if any(vision_model.lower() in model.lower() for vision_model in vision_models)
        ]
        if not available_vision_models:
            log_message("warning", "No vision-capable models found. Please install a vision model like llava:latest")
            return []
        return available_vision_models
    except requests.exceptions.RequestException as e:
        log_message("error", f"Failed to fetch models from Ollama: {e}")
        return []

def get_user_input() -> tuple:
    """Get user preferences for processing"""
    import sys
    print("\n[Image Analysis Configuration]")
    if not sys.stdin.isatty():
        log_message("warning", "No interactive terminal detected. Using defaults.")
        process_all = True
        models = get_available_models()
        selected_model = models[0] if models else "llava:latest"
        prompt = DEFAULT_PROMPT
        return process_all, selected_model, prompt

    console.print("\n[bold cyan]Image Analysis Configuration[/bold cyan]")
    process_all = console.input("\nDo you want to analyze all images in the directory? (y/n): ").lower() == 'y'
    models = get_available_models()
    if not models:
        log_message("warning", "Using default model 'llava:latest'. Please ensure it's installed.")
        return process_all, "llava:latest", None
    console.print("\n[bold]Available vision-capable models:[/bold]")
    for idx, model in enumerate(models, 1):
        console.print(f"{idx}. {model}")
    while True:
        try:
            model_idx = int(console.input("\nSelect model number: ")) - 1
            if 0 <= model_idx < len(models):
                selected_model = models[model_idx]
                break
            console.print("[red]Invalid selection. Please try again.[/red]")
        except ValueError:
            console.print("[red]Please enter a valid number.[/red]")
    use_custom_prompt = console.input("\nDo you want to use a custom prompt? (y/n): ").lower() == 'y'
    prompt = console.input("\nEnter your custom prompt: ") if use_custom_prompt else DEFAULT_PROMPT
    return process_all, selected_model, prompt

def select_image(path: str) -> str:
    """Allow user to select a single image from directory"""
    image_files = [f for f in os.listdir(path) if f.lower().endswith(SUPPORTED_EXTENSIONS)]

    if not image_files:
        log_message("error", "No images found in directory")
        return ""

    console.print("\n[bold]Available images:[/bold]")
    for idx, img in enumerate(image_files, 1):
        console.print(f"{idx}. {img}")

    while True:
        try:
            img_idx = int(console.input("\nSelect image number: ")) - 1
            if 0 <= img_idx < len(image_files):
                return os.path.join(path, image_files[img_idx])
            console.print("[red]Invalid selection. Please try again.[/red]")
        except ValueError:
            console.print("[red]Please enter a valid number.[/red]")

# Main
if __name__ == "__main__":
    # Set default image path
    image_path = "./data"  # Default path

    # Ensure data directory exists
    ensure_directory_exists(image_path)

    log_message("start", "Starting image processing application...")

    # Interactive configuration for model and prompt
    process_all, selected_model, custom_prompt = get_user_input()
    if process_all:
        process_images(image_path, custom_prompt, selected_model)
    else:
        # Allow user to select a single image
        selected_image = select_image(image_path)
        if selected_image:
            process_images(selected_image, custom_prompt, selected_model)

    log_message("completion", "All tasks completed!")
