import psutil
import platform
import time
from typing import Dict, Tuple, Optional

class OllamaKiller:
    """
    A ComfyUI node for managing Ollama processes with enhanced process handling.
    Provides cross-platform support and detailed process management.
    """
    def __init__(self):
        self.type = "ollama_killer"
        # Platform-specific process names
        self.process_names = {
            'Windows': 'ollama.exe',
            'Darwin': 'ollama',  # macOS
            'Linux': 'ollama'
        }
        self.platform = platform.system()
        self.task_name = self.process_names.get(self.platform, 'ollama')
        self.timeout = 5  # seconds to wait for process termination
        
    @classmethod
    def INPUT_TYPES(cls) -> Dict:
        """
        Define the input types for the node.
        """
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}), # 'text' is the input name
                "trigger": ("BOOLEAN", {
                    "default": False,
                    "label_on": "Kill Process",
                    "label_off": "Idle"
                })
            },
            "optional": {
                "force_kill": (["false", "true"], { # ComfyUI handles string booleans well
                    "default": "false",
                    "label": "Force Kill"
                })
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("status", "output_text") # output_text will be the original 'text' input
    OUTPUT_NODE = True
    FUNCTION = "kill_ollama"
    CATEGORY = "utils"

    def _terminate_process(self, process: psutil.Process, force: bool = False) -> Tuple[bool, str]:
        """
        Terminate a process gracefully, with optional force kill.
        Returns (success, message)
        """
        try:
            # Try graceful termination first
            process.terminate()
            try:
                process.wait(timeout=self.timeout)
                return True, f"Process terminated (PID: {process.pid})"
            except psutil.TimeoutExpired:
                if force:
                    process.kill()
                    return True, f"Process force killed (PID: {process.pid})"
                return False, f"Process did not terminate in time (PID: {process.pid})"
            except psutil.NoSuchProcess:
                # Process might have terminated just after .terminate() was called
                return True, f"Process already terminated (PID: {process.pid})"
        except Exception as e:
            # Catch other potential errors during termination attempts
            return False, f"Failed to terminate process (PID: {process.pid}): {str(e)}"

    def kill_ollama(self, text: str, trigger: bool, force_kill: str = "false") -> Tuple[str, str]:
        """
        Main function to find and terminate Ollama processes.
        Returns (status, original_text)
        """
        # Node acts only when 'trigger' is True
        if not trigger:
            return "Idle", text

        status_messages = []
        force = force_kill.lower() == "true" # Convert string input to boolean
        processes_found = 0
        processes_terminated = 0

        try:
            # Step 1: Identify all target processes first
            # This minimizes race conditions where a process might die
            # between finding and attempting to kill
            target_processes = []
            for proc in psutil.process_iter(['pid', 'name']): # 'cmdline' not strictly needed here
                try:
                    proc_name = proc.info['name'] or ''
                    if proc_name.lower() == self.task_name.lower():
                        processes_found += 1
                        target_processes.append(proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # Skip processes that are already gone, inaccessible, or zombified
                    continue

            # Step 2: Attempt to terminate identified processes
            for proc in target_processes:
                try:
                    success, message = self._terminate_process(proc, force)
                    if success:
                        processes_terminated += 1
                        status_messages.append(f"✓ {message}")
                    else:
                        status_messages.append(f"✗ {message}")
                except Exception as e:
                    # General error if something unexpected happens during _terminate_process call
                    status_messages.append(f"✗ Error handling process (PID: {proc.info.get('pid', 'N/A')}): {str(e)}")

            # Step 3: Compile overall status message
            if processes_found == 0:
                status = f"No {self.task_name} processes found."
            elif processes_terminated == processes_found:
                status = f"Successfully terminated {processes_terminated} of {processes_found} process(es)."
            else:
                status = f"Terminated {processes_terminated} of {processes_found} process(es). Some failed."

            # Append detailed messages if any
            if status_messages:
                status += "\n" + "\n".join(status_messages)

            # Return status and original text input
            return status, text # FIXED: Changed text_input to text

        except Exception as e:
            # Catch any high-level errors during the execution of kill_ollama
            return f"Error: {str(e)}", text # FIXED: Changed text_input to text

# This is important for ComfyUI to recognize and load the node
NODE_CLASS_MAPPINGS = {
    "OllamaKiller": OllamaKiller
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OllamaKiller": "Ollama Process Killer"
}