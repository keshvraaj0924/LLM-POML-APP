# # poml_app/services/poml_runner.py
from poml.integration.langchain import LangchainPomlTemplate

class POMLRunner:
    @staticmethod
    def run_prompt(prompt_path: str, **kwargs) -> str:
        """
        Load a POML prompt file, render it with given parameters, and return the final text.
        """
        try:
            # Use the official POML LangChain integration
            template = LangchainPomlTemplate.from_file(prompt_path, speaker_mode=False)
            result = template.format(**kwargs)
            
            # Ensure we return a string
            if hasattr(result, 'content'):
                return result.content
            elif hasattr(result, 'to_string'):
                return result.to_string()
            else:
                return str(result)
                
        except Exception as e:
            print(f"POML Error: {e}")
            # Fallback to simple string replacement
            with open(prompt_path, "r", encoding="utf-8") as f:
                poml_content = f.read()
            
            # Replace template variables manually
            for key, value in kwargs.items():
                poml_content = poml_content.replace(f"{{{key}}}", str(value))
            
            return poml_content
