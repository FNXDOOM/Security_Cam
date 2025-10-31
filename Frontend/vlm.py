import numpy as np
import cv2
from collections import deque
import time
import random

# Try to import optional dependencies
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    print("⚠️ PyTorch not available. Using CPU-only mode.")
    TORCH_AVAILABLE = False

try:
    from transformers import AutoProcessor, AutoModelForCausalLM
    from PIL import Image
    TRANSFORMERS_AVAILABLE = True
    print("✅ Transformers available - SmolVLM2 enabled")
except ImportError:
    print("⚠️ Transformers not available. Install with: pip install transformers pillow")
    print("   Falling back to basic violation descriptions...")
    TRANSFORMERS_AVAILABLE = False

class SmolVLM2Manager:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.processor = None
            self.model = None
            self.device = "cuda" if TORCH_AVAILABLE and torch.cuda.is_available() else "cpu"
            self.enabled = TRANSFORMERS_AVAILABLE
            self.recent_captions = deque(maxlen=10)
            self.violation_counter = 0
            SmolVLM2Manager._initialized = True
    
    def load_models(self):
        """Load models only when needed and if transformers is available."""
        if not self.enabled:
            print("⚠️ SmolVLM2 not available. Using fallback descriptions.")
            return False
            
        if self.processor is None or self.model is None:
            print("🤖 Loading SmolVLM2 models...")
            try:
                model_options = [
                    "HuggingFaceTB/SmolVLM-500M-Instruct",
                    "HuggingFaceTB/SmolVLM-1.7B-Instruct"
                ]
                
                model_name = None
                for model_option in model_options:
                    try:
                        print(f"   Trying model: {model_option}")
                        test_processor = AutoProcessor.from_pretrained(model_option, trust_remote_code=True)
                        model_name = model_option
                        print(f"   ✅ Found working model: {model_name}")
                        break
                    except Exception as e:
                        print(f"   ❌ Model {model_option} not available: {str(e)[:100]}...")
                        continue
                
                if model_name is None:
                    print("❌ No SmolVLM model found")
                    self.enabled = False
                    return False
                
                self.processor = AutoProcessor.from_pretrained(model_name, trust_remote_code=True)
                
                if self.device == "cuda" and torch.cuda.is_available():
                    self.model = AutoModelForCausalLM.from_pretrained(
                        model_name,
                        torch_dtype=torch.float16,
                        device_map="auto",
                        trust_remote_code=True
                    )
                else:
                    self.model = AutoModelForCausalLM.from_pretrained(
                        model_name,
                        torch_dtype=torch.float32,
                        trust_remote_code=True
                    ).to(self.device)
                
                self._model_name = model_name
                print(f"✅ SmolVLM loaded successfully on {self.device}")
            except Exception as e:
                print(f"❌ Error loading SmolVLM2: {e}")
                print("   Falling back to basic descriptions...")
                self.enabled = False
                return False
        return True
    
    def generate_caption(self, image, prompt="Describe this security situation in detail, focusing on people and any weapons visible:"):
        """Generate caption for a single image using SmolVLM."""
        if not self.enabled or not self.load_models():
            return self._generate_basic_caption()
        
        try:
            if isinstance(image, np.ndarray):
                if len(image.shape) == 3 and image.shape[2] == 3:
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
            
            inputs = self.processor(images=image, text=prompt, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                generated_ids = self.model.generate(
                    **inputs,
                    max_new_tokens=50,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.processor.tokenizer.eos_token_id
                )
            
            generated_text = self.processor.decode(generated_ids[0], skip_special_tokens=True)
            
            if prompt in generated_text:
                caption = generated_text.split(prompt)[-1].strip()
            else:
                caption = generated_text.strip()
            
            return caption if caption else "Security monitoring detected potential threat."
            
        except Exception as e:
            print(f"❌ Error generating caption with SmolVLM: {e}")
            return self._generate_basic_caption()
    
    def _generate_basic_caption(self):
        """Fallback method for diverse basic violation descriptions."""
        timestamp = int(time.time())
        hour = int(time.strftime("%H"))
        
        time_contexts = {
            'morning': (6, 11),
            'midday': (12, 14), 
            'afternoon': (15, 17),
            'evening': (18, 22)
        }
        
        time_period = 'monitoring hours'
        for period, (start, end) in time_contexts.items():
            if start <= hour <= end:
                time_period = period
                break
        
        description_templates = [
            f"Security alert: Individual detected carrying weapon during {time_period}",
            f"Weapon detection: Person observed with potential weapon - immediate response required",
            f"Critical security breach: Armed individual identified in monitored area",
            f"Threat detected: Person carrying weapon requires urgent security intervention",
            f"High-priority alert: Weapon possession detected - security team notified",
            f"Security violation: Armed person detected in restricted area",
            f"Weapon threat identified: Individual with weapon requires immediate attention",
            f"Critical incident: Person with weapon detected by security monitoring system"
        ]
        
        environmental_additions = [
            "in monitored zone",
            "near restricted area",
            "in public space", 
            "during active monitoring",
            "in security-sensitive location",
            "within surveillance perimeter"
        ]
        
        base_desc = random.choice(description_templates)
        
        if timestamp % 10 < 3:
            env_context = random.choice(environmental_additions)
            if 'zone' not in base_desc.lower() and 'area' not in base_desc.lower():
                base_desc += f" {env_context}"
        
        return base_desc
    
    def clear_cache(self):
        """Clear GPU memory cache."""
        if TORCH_AVAILABLE and torch.cuda.is_available():
            torch.cuda.empty_cache()

# Initialize a single instance to be imported by other modules
vlm_manager = SmolVLM2Manager()