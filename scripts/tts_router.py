"""
TTS Router — Route between free GPU providers for Qwen3 TTS
"""

import os
import yaml
import numpy as np
import soundfile as sf
from pathlib import Path

class TTSRouter:
    """Route TTS requests between Kaggle, Colab, and Vultr."""
    
    def __init__(self):
        self.providers = {
            "kaggle": {"gpu": "T4", "free_hours_week": 30, "session_limit": 9},
            "colab": {"gpu": "T4", "free_hours_week": 15, "session_limit": 12},
            "vultr": {"gpu": "A40", "free_credits": 250, "cost_per_hour": 0.18}
        }
        self.usage = {"kaggle": 0, "colab": 0, "vultr": 0}
        self.model = None
        self.current_provider = None
    
    def get_provider(self):
        """Route to the provider with the most free hours left."""
        if self.usage["kaggle"] < 30 * 7:
            return "kaggle"
        if self.usage["colab"] < 15 * 7:
            return "colab"
        if self.usage["vultr"] < 250 / 0.18:
            return "vultr"
        return None
    
    def load_model(self, provider=None):
        """Load Qwen3 TTS model."""
        if provider is None:
            provider = self.get_provider()
        
        if provider is None:
            raise Exception("All free tiers exhausted")
        
        print(f"Loading model on {provider}...")
        
        from qwen_tts import Qwen3TTSModel
        
        self.model = Qwen3TTSModel.from_pretrained(
            "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
            torch_dtype="auto",
            device_map="auto"
        )
        
        self.current_provider = provider
        print(f"Model loaded on {provider}!")
    
    def design_voice(self, text, instruct):
        """Design a new voice."""
        if self.model is None:
            self.load_model()
        
        voice = self.model.voice_design(text=text, instruct=instruct)
        return voice
    
    def generate(self, text, voice, rate=-0.3):
        """Generate TTS audio."""
        if self.model is None:
            self.load_model()
        
        output = self.model.generate(text=text, voice=voice, rate=rate)
        
        # Update usage
        self.usage[self.current_provider] += len(output.audio) / output.sample_rate / 3600
        
        return output.audio, output.sample_rate
    
    def save_audio(self, audio, sample_rate, filename):
        """Save audio to file."""
        sf.write(filename, audio, sample_rate)
        print(f"Saved: {filename}")
    
    def get_usage_report(self):
        """Get usage report for all providers."""
        report = {}
        for provider, hours in self.usage.items():
            limit = self.providers[provider].get("free_hours_week", 0) * 7
            if limit > 0:
                report[provider] = {
                    "used_hours": round(hours, 2),
                    "limit_hours": limit,
                    "remaining_hours": round(limit - hours, 2),
                    "percent_used": round(hours / limit * 100, 1)
                }
        return report


# Voice registry loader
def load_voice_registry():
    """Load voice registry from YAML."""
    registry_path = Path(__file__).parent.parent / "voices" / "registry.yaml"
    with open(registry_path) as f:
        return yaml.safe_load(f)

def get_voice_for_shelf(shelf, registry):
    """Get the primary voice for a shelf."""
    shelf_config = registry["shelves"].get(shelf, {})
    primary_voice_id = shelf_config.get("primary_voice")
    
    if primary_voice_id is None:
        return None  # No voice for this shelf (e.g., PLACE)
    
    for voice in registry["voices"]:
        if voice["id"] == primary_voice_id:
            return voice
    
    return None

def update_voice_metrics(voice_id, video_metrics, registry):
    """Update voice metrics from YouTube API data."""
    for voice in registry["voices"]:
        if voice["id"] == voice_id:
            voice["metrics"]["videos_used"] += 1
            voice["metrics"]["avg_watch_time"] = (
                (voice["metrics"]["avg_watch_time"] * (voice["metrics"]["videos_used"] - 1) +
                 video_metrics["watch_time"]) / voice["metrics"]["videos_used"]
            )
            voice["metrics"]["retention_rate"] = video_metrics["retention_rate"]
            voice["metrics"]["subscriber_growth"] += video_metrics["new_subscribers"]
            break
    
    # Save updated registry
    registry_path = Path(__file__).parent.parent / "voices" / "registry.yaml"
    with open(registry_path, 'w') as f:
        yaml.dump(registry, f, default_flow_style=False)


# Example usage
if __name__ == "__main__":
    router = TTSRouter()
    
    # Load voice registry
    registry = load_voice_registry()
    
    # Get voice for Spiritual Sleep
    voice = get_voice_for_shelf("SPIRITUAL", registry)
    print(f"Using voice: {voice['name']}")
    
    # Design the voice
    designed_voice = router.design_voice(
        text="Welcome to Spiritual Sleep.",
        instruct=voice["description"]
    )
    
    # Generate test audio
    audio, sample_rate = router.generate(
        text="Salary. From Latin salarium. Salt money. Roman soldiers were paid in salt.",
        voice=designed_voice
    )
    
    # Save
    router.save_audio(audio, sample_rate, "test_output.wav")
    
    # Print usage
    print("\nUsage report:")
    for provider, stats in router.get_usage_report().items():
        print(f"  {provider}: {stats['used_hours']:.1f}/{stats['limit_hours']} hours ({stats['percent_used']}%)")
