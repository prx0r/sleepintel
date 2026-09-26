"""
Voice Matcher — JEV-native voice selection for sleepintel
Matches content to compatible voices based on shelf, engine, mood, and performance.
"""
import os
import yaml
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
VOICES_DIR = ROOT / "voices"

def load_registry():
    """Load voice registry from YAML."""
    with open(VOICES_DIR / "registry.yaml") as f:
        return yaml.safe_load(f)

def get_compatible_voices(channel, registry=None):
    """Get all voices compatible with a channel's shelf and engine."""
    if registry is None:
        registry = load_registry()
    
    shelf = channel.get("shelf")
    engine_sub = channel.get("sub")  # e.g., "E2a"
    
    compatible = []
    for voice in registry["voices"]:
        # Check shelf compatibility
        shelf_match = shelf in voice.get("shelves", [])
        
        # Check engine compatibility
        engine_match = engine_sub in voice.get("compatible_engines", [])
        
        if shelf_match and engine_match:
            compatible.append(voice)
    
    return compatible

def score_voice(voice, channel):
    """Score a voice for a specific channel based on multiple factors."""
    score = 0.0
    
    # 1. Shelf match (required - already filtered)
    score += 0.3
    
    # 2. Engine match (required - already filtered)
    score += 0.2
    
    # 3. Mood overlap with channel tags
    channel_tags = set(channel.get("tags", []))
    voice_mood = set(voice.get("mood", []))
    mood_overlap = len(channel_tags & voice_mood)
    score += min(mood_overlap * 0.1, 0.2)
    
    # 4. Performance metrics (if available)
    metrics = voice.get("metrics", {})
    if metrics.get("total_videos", 0) > 0:
        # Higher retention = better
        retention = metrics.get("avg_retention_rate", 0)
        score += retention * 0.15
        
        # Higher views per video = better
        views_per_video = metrics.get("avg_views_per_video", 0)
        if views_per_video > 1000:
            score += 0.1
        elif views_per_video > 500:
            score += 0.05
    
    # 5. Voice effort (lower effort = better for scale)
    effort = channel.get("effort", 5)
    if effort <= 3:
        score += 0.1  # Low effort channels get bonus
    
    return round(score, 3)

def select_voice(channel, registry=None, top_n=4):
    """Select the best voice for a channel. Returns top N candidates."""
    if registry is None:
        registry = load_registry()
    
    compatible = get_compatible_voices(channel, registry)
    
    if not compatible:
        # Fallback to shelf primary
        shelf = channel.get("shelf")
        primary_id = registry["shelves"].get(shelf, {}).get("primary_voice")
        if primary_id:
            for v in registry["voices"]:
                if v["id"] == primary_id:
                    return [v]
        return []
    
    # Score each voice
    scored = [(score_voice(v, channel), v) for v in compatible]
    scored.sort(key=lambda x: x[0], reverse=True)
    
    return [v for _, v in scored[:top_n]]

def get_voice_stats(voice_id, registry=None):
    """Get detailed stats for a voice."""
    if registry is None:
        registry = load_registry()
    
    for voice in registry["voices"]:
        if voice["id"] == voice_id:
            return voice.get("metrics", {})
    
    return {}

def update_voice_stats(voice_id, video_data, registry=None):
    """Update voice stats after a video is published."""
    if registry is None:
        registry = load_registry()
    
    for voice in registry["voices"]:
        if voice["id"] == voice_id:
            metrics = voice["metrics"]
            
            # Update counters
            metrics["total_videos"] += 1
            metrics["total_watch_time_hours"] += video_data.get("watch_time_hours", 0)
            metrics["total_views"] += video_data.get("views", 0)
            metrics["total_subscriber_growth"] += video_data.get("subscriber_growth", 0)
            
            # Update averages
            n = metrics["total_videos"]
            metrics["avg_watch_time_minutes"] = round(
                metrics["total_watch_time_hours"] * 60 / n, 1
            ) if n > 0 else 0
            metrics["avg_views_per_video"] = round(
                metrics["total_views"] / n, 0
            ) if n > 0 else 0
            
            # Update retention (running average)
            old_retention = metrics["avg_retention_rate"]
            new_retention = video_data.get("retention_rate", 0)
            metrics["avg_retention_rate"] = round(
                (old_retention * (n - 1) + new_retention) / n, 3
            ) if n > 0 else new_retention
            
            # Update shelf counts
            shelf = video_data.get("shelf")
            if shelf:
                metrics["videos_by_shelf"][shelf] = metrics["videos_by_shelf"].get(shelf, 0) + 1
            
            # Update engine counts
            engine = video_data.get("engine")
            if engine:
                metrics["videos_by_engine"][engine] = metrics["videos_by_engine"].get(engine, 0) + 1
            
            # Track best/worst
            if metrics["best_performing_video"] is None or video_data.get("views", 0) > metrics["best_performing_video"].get("views", 0):
                metrics["best_performing_video"] = {
                    "video_id": video_data.get("video_id"),
                    "views": video_data.get("views", 0),
                    "title": video_data.get("title", "")
                }
            
            if metrics["worst_performing_video"] is None or video_data.get("views", 0) < metrics["worst_performing_video"].get("views", 0):
                metrics["worst_performing_video"] = {
                    "video_id": video_data.get("video_id"),
                    "views": video_data.get("views", 0),
                    "title": video_data.get("title", "")
                }
            
            # Save registry
            with open(VOICES_DIR / "registry.yaml", 'w') as f:
                yaml.dump(registry, f, default_flow_style=False)
            
            return metrics
    
    return None


# Example usage
if __name__ == "__main__":
    registry = load_registry()
    
    # Example channel
    channel = {
        "id": 1,
        "name": "Steiner Sleep",
        "shelf": "ESOTERIC",
        "sub": "E2a",
        "tags": ["type-reading"],
        "effort": 3
    }
    
    # Get compatible voices
    compatible = get_compatible_voices(channel, registry)
    print(f"Compatible voices for {channel['name']}:")
    for v in compatible:
        print(f"  {v['id']}: {v['name']} — {v['persona']}")
    
    # Select best voice
    best = select_voice(channel, registry, top_n=3)
    print(f"\nTop 3 voices:")
    for i, v in enumerate(best, 1):
        score = score_voice(v, channel)
        print(f"  {i}. {v['name']} (score: {score})")
    
    # Get stats
    print(f"\nStats for {best[0]['name']}:")
    stats = get_voice_stats(best[0]["id"], registry)
    for key, value in stats.items():
        if not isinstance(value, dict):
            print(f"  {key}: {value}")
