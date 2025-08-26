# import subprocess
# import json

# class OllamaClient:
#     def __init__(self, model="mistral"):
#         self.model = model

#     def query(self, prompt: str) -> str:
#         result = subprocess.run(
#             ["ollama", "run", self.model],
#             input=prompt,
#             text=True,
#             capture_output=True
#         )
#         return result.stdout.strip()

import subprocess
import json

class OllamaClient:
    def __init__(self, model="mistral"):
        self.model = model

    def query(self, prompt: str) -> str:
        # Debug what we're receiving
        print(f"DEBUG - Prompt type: {type(prompt)}")
        print(f"DEBUG - Prompt preview: {repr(prompt[:100])}")
        
        # Ensure prompt is a string
        if isinstance(prompt, list):
            prompt = '\n'.join(str(item) for item in prompt)
        elif not isinstance(prompt, str):
            prompt = str(prompt)
        
        try:
            result = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt,
                text=True,
                capture_output=True,
                encoding='utf-8',  # Explicit encoding to fix Unicode issues
                errors='replace'   # Handle encoding errors gracefully
            )
            
            if result.returncode != 0:
                print(f"Ollama error: {result.stderr}")
                return "Error: Could not get response from Ollama"
            
            return result.stdout.strip()
            
        except Exception as e:
            print(f"Subprocess error: {e}")
            return f"Error: {str(e)}"

