
# OllamaKiller Node for ComfyUI

**OllamaKiller** is a utility node for ComfyUI designed to manage VRAM usage more efficiently by automatically terminating the `ollama_llama_server.exe` process. This is particularly useful for users with limited VRAM, allowing them to clear up memory after running models and improve workflow performance.

## Purpose

Running `ollama_llama_server.exe` in ComfyUI workflows can consume 2–3 GB of VRAM or more, depending on the model. The OllamaKiller node automatically kills this process after each use, freeing up valuable memory and enhancing performance in subsequent generations.

## How It Works

When any text or prompt flows through the OllamaKiller node, it searches for `ollama_llama_server.exe` and terminates it if running. This frees VRAM after the model has completed its task, allowing smoother transitions between models in workflows without needing manual process management.

## Installation

1. **Clone the Repository**:
   Clone the OllamaKiller repository into your ComfyUI `custom_nodes` directory:
   ```bash
   git clone https://github.com/mithamunda/ComfyUI-ollama_killer.git
   ```
2. **Restart ComfyUI**:
   Restart ComfyUI to load the newly added node.

3. **Verify Installation**:
   The OllamaKiller node should now appear in the **utils** category in ComfyUI.

## Usage

1. **Add OllamaKiller to Your Workflow**:
   Insert the OllamaKiller node after any point where the `ollama_llama_server.exe` process is no longer needed.

2. **Automatic Trigger**:
   When any text or prompt flows through the node, it triggers the termination process for `ollama_llama_server.exe`, freeing up VRAM automatically.

3. **Benefits**:
   - **Free Up VRAM**: Frees VRAM used by the Ollama process after completion, enhancing speed and efficiency for the next step in your workflow.
   - **Automated Process Control**: No manual intervention needed—simply run your workflow, and OllamaKiller handles process termination.

## Node Information

- **Node Class**: `OllamaKiller`
- **Category**: `utils`
- **Input Type**: Any text or prompt (String)
- **Output Type**: Confirmation message (STRING) about the termination status of `ollama_llama_server.exe`.

## Example Workflow

1. Load and run a model in ComfyUI.
2. Place the OllamaKiller node after your model in the workflow to free up VRAM.
3. Run the workflow; the node will automatically terminate `ollama_llama_server.exe` and output a success message, allowing you to continue without manual memory management.

## License

This code is open-source and free to use for VRAM optimization in ComfyUI. Contributions to enhance functionality are welcome!
