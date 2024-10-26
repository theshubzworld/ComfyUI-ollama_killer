import psutil
import subprocess

class OllamaKiller:
    def __init__(self):
        self.type = "ollama_killer"
        self.task_name = "ollama_llama_server.exe"
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "trigger_text": ("STRING", {"default": "", "multiline": False}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "kill_ollama"
    CATEGORY = "utils"
    
    def kill_ollama(self, trigger_text):
        try:
            killed = False
            # Iterate through all running processes
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    # Check if process name matches
                    if proc.info['name'].lower() == self.task_name.lower():
                        # Kill the process
                        process = psutil.Process(proc.info['pid'])
                        process.terminate()
                        killed = True
                        return (f"Successfully terminated {self.task_name} (PID: {proc.info['pid']})",)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
                
            if not killed:
                return (f"Process {self.task_name} not found.",)
                
        except Exception as e:
            return (f"Error: {str(e)}",)

# This is important for ComfyUI to recognize and load the node
NODE_CLASS_MAPPINGS = {
    "OllamaKiller": OllamaKiller
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OllamaKiller": "Ollama Process Killer"
}