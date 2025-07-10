# Ollama Image Processing CLI Tool

A flexible command-line tool for analyzing images using local vision-capable Ollama models. This tool supports advanced image preprocessing, customizable prompts, and is ideal for extracting structured information from images such as invoices, receipts, documents, or general photos.

---

## What This Project Does

- **Batch or Single Image Processing:** Analyze all images in a directory or select a specific image for processing.
- **Image Preprocessing:** Automatically resizes and converts images to a consistent format for optimal model input.
- **Custom Instructions:** Provide your own prompt to tailor the analysis (e.g., extract invoice fields, summarize a document, describe a scene).
- **Vision Model Selection:** Choose from any installed vision-capable Ollama model (e.g., `gemma3:4b`, `llava:latest`, `qwen-vl`).
- **Structured Output:** Results are saved to timestamped text files in the `outputs` directory, with clear formatting for downstream use.
- **Rich Logging:** Progress and results are displayed with categorized, color-coded feedback.

---

## Example Use Cases

- **Invoice/Receipt Extraction:**  
  Use a prompt like:  
  `Extract all key fields from this invoice, including invoice number, date, total, and vendor.`

- **Document Summarization:**  
  Use a prompt like:  
  `Summarize the main points of this document and list any visible headings.`

- **General Image Description:**  
  Use a prompt like:  
  `Describe this image, highlighting any notable details (including visible text).`

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/tristan-mcinnis/Ollama-Image-Processing-CLI-Tool.git
    cd Ollama-Image-Processing-CLI-Tool
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure your local Ollama API server is running at `http://localhost:11434`.

---

## Usage

1. **Prepare Images:**  
   Place images to be processed in the `./data` directory (created automatically if missing).

2. **Run the Tool:**  
   ```bash
   python3 main.py
   ```

3. **Interactive Configuration:**  
   - Choose to process all images or select a specific image.
   - Select from available vision-capable models.
   - Enter a custom prompt or use the default.

4. **Review Results:**  
   - Processed results are saved in the `./outputs` directory with timestamped filenames.
   - Output includes the model used, prompt, and extracted information for each image.

---

## Supported Image Formats

- JPG, PNG, BMP, TIFF, HEIC, GIF, WEBP, and more.

---

## Supported Models

Any vision-capable Ollama model, including but not limited to:
- `gemma3:4b`
- `gemma3:12b`
- `gemma3:27b`
- `llava:latest`
- `llava-phi3`
- `qwen-vl`
- Others with multimodal (text, image) support

---

## Requirements

- Python 3.8+
- Local Ollama API server running at `http://localhost:11434`
- At least one vision-capable model installed in Ollama

---

## Customizing Prompts for Specific Objects

You can tailor the prompt to the object in the image. For example:
- **Invoice:**  
  `Extract invoice number, date, total, and vendor from this invoice.`
- **Receipt:**  
  `List all purchased items, quantities, and total amount from this receipt.`
- **Document:**  
  `Summarize the document and extract all headings.`
- **Photo:**  
  `Describe the scene and list any visible objects or text.`

---

## Output

- Results are saved in the `outputs` directory, one file per run, with clear separation for each image.
- Each output includes the image filename, extracted or described content, and the prompt/model used.

---

## License

MIT License
