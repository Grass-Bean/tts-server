# 🗣️ tts-server

A simple server for hosting a [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) instance using [Litserve](https://lightning.ai/docs/litserve/home). Built with speed in mind and packaged with [`uv`](https://github.com/astral-sh/uv).

The code was adapted from the following [pytorch lightning guide](https://lightning.ai/sitammeur/studios/deploy-kokoro-tts-model?section=featured).

## 🧰 Tech Stack

- Python (for the programming language)
- PyTorch (for the deep learning framework)
- Hugging Face Transformers Library (for the model)
- LitServe (for the serving engine)

## 🚀 Features

- Fast and lightweight TTS server powered by Kokoro TTS
- Fully in-memory audio processing
- Served via `litserve` for easy REST API usage  
- Dependency management with `uv`
- Simple startup via Windows `.bat` file  

---

## 📦 Installation

1. **Clone the repository**
   ```
   git clone https://github.com/Grass-Bean/tts-server.git
   cd tts-server
   ```

2. **Create Virtual Environment**
    ```
    uv venv
    .venv\Scripts\Activate
    ```

3. **Install dependencies (except torch)**
    ```
    uv sync
    ```

4. **Manually install PyTorch**
    Visit https://pytorch.org/get-started/locally and install the appropriate version for your system.

    Example (CUDA 12.6):
    ```
    uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
    ```

5. **Run the server Run the provided .bat file:**
    ```
    start_server.bat
    ```

---

## 🧪 Example Usage

Once running, your TTS server should be available at:
```
http://localhost:8000
```

You can test it using the included client.bat:
```
run_client.bat
```

Make sure the server is running before executing the client. The client will send a sample request and handle the TTS response. You will find an output.wav file in the tts-server directory. 

You may adapt the included client.py file for your specific use case.

---

## ⚠️ Notes

- PyTorch must be installed manually due to platform-specific wheels

- Requires Python 3.11+

- Developed and tested on Windows. Unix support can be added with minor changes

- Might break if cpu torch version is installed on device with gpu when accelerator is set to 'auto' in main.py

- Limited support for long audio. Please include regular punctuation in sentences or the output speech will get truncated

---

## 📄 License

MIT License – see [LICENSE file](LICENSE) for details.