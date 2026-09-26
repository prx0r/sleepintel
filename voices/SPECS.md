# Voice Specs — 10 reusable voices for the sleep network

## Design Principles

1. **Each voice is a character** — not just a sound, but a persona
2. **Compatibility is multi-dimensional** — voice matches content on shelf, mood, pace, accent
3. **Stats are granular** — every video the voice is used on contributes metrics
4. **JEV-native** — voice selection uses choice/noul primitives

---

## The 10 Voices

### V01 — The Sage
```yaml
id: V01
name: "The Sage"
persona: "Ancient wisdom keeper. Speaks from experience, not theory."
instruct: "Deep, warm male voice. Slow, measured pace. British accent. Slight gravel. Authoritative but kind. Like a favorite professor who also reads poetry."
gender: male
accent: british
pitch: low
pace: slow
mood: [wise, calm, authoritative, warm]
shelves: [SPIRITUAL, ESOTERIC]
content_types: [reading, journey, essay]
compatible_with: [E2a, E2c, E3a, E5a]
```

### V02 — The Storyteller
```yaml
id: V02
name: "The Storyteller"
persona: "Fireside narrator. Makes every tale feel personal."
instruct: "Soft, gentle female voice. Warm tone. Slight smile in the voice. Like reading to someone you love. European accent, slightly old-fashioned."
gender: female
accent: european
pitch: medium
pace: slow
mood: [warm, cozy, intimate, gentle]
shelves: [STORY]
content_types: [reading, essay]
compatible_with: [E2a, E2c, E5a]
```

### V03 — The Lecturer
```yaml
id: V03
name: "The Lecturer"
persona: "Clear teacher. Makes complex things simple without dumbing them down."
instruct: "Clear, neutral male voice. Precise, technical. American accent. Calm authority. Like a professor who genuinely loves the subject."
gender: male
accent: american
pitch: medium
pace: measured
mood: [clear, precise, educational, calm]
shelves: [MIND]
content_types: [essay, reference, procedural]
compatible_with: [E5a, E5b, E5c, E5d]
```

### V04 — The Mystic
```yaml
id: V04
name: "The Mystic"
persona: "Keeper of hidden knowledge. Speaks as if revealing secrets."
instruct: "Deep, resonant voice. Mysterious, measured pace. Slight echo in the tone. Like someone who has seen things they cannot fully describe."
gender: male
accent: neutral
pitch: very_low
pace: very_slow
mood: [mysterious, deep, profound, hypnotic]
shelves: [ESOTERIC, SPIRITUAL]
content_types: [reading, journey]
compatible_with: [E2a, E3a, E3b]
```

### V05 — The Healer
```yaml
id: V05
name: "The Healer"
persona: "Compassionate presence. Makes you feel safe and understood."
instruct: "Warm, friendly female voice. Gentle, caring tone. Like a therapist who genuinely cares. Soft, never sharp."
gender: female
accent: neutral
pitch: medium
pace: slow
mood: [warm, caring, safe, hopeful]
shelves: [FRESH, STORY]
content_types: [daily, essay, reading]
compatible_with: [E5a, E6a, E2a]
```

### V06 — The Philosopher
```yaml
id: V06
name: "The Philosopher"
persona: "Thinks aloud. Each sentence is a meditation."
instruct: "Measured, thoughtful male voice. Slightly hesitant, as if thinking in real-time. European accent. Like someone working through ideas slowly."
gender: male
accent: european
pitch: medium
pace: very_slow
mood: [contemplative, thoughtful, probing, calm]
shelves: [ESOTERIC, MIND]
content_types: [essay, reading]
compatible_with: [E5a, E2a, E2c]
```

### V07 — The Navigator
```yaml
id: V07
name: "The Navigator"
persona: "Guides you through places and times. Never rushes."
instruct: "Clear, steady female voice. Calm, directional tone. Like a museum guide who loves their work. Slight warmth, never cold."
gender: female
accent: neutral
pitch: medium
pace: measured
mood: [steady, directional, calm, guiding]
shelves: [STORY, MIND]
content_types: [essay, reference, procedural]
compatible_with: [E5a, E5c, E5d, E5e]
```

### V08 — The Dreamer
```yaml
id: V08
name: "The Dreamer"
persona: "Lives between waking and sleeping. Every word floats."
instruct: "Soft, breathy female voice. Ethereal quality. Like someone speaking from a dream. Very slow, very gentle. Almost whispering."
gender: female
accent: neutral
pitch: high
pace: very_slow
mood: [ethereal, dreamy, soft, floating]
shelves: [SPIRITUAL, STORY]
content_types: [journey, reading]
compatible_with: [E3a, E3b, E2a]
```

### V09 — The Archivist
```yaml
id: V09
name: "The Archivist"
persona: "Reads from ancient texts with reverence. Each word matters."
instruct: "Deep, formal male voice. Precise pronunciation. British accent. Like reading from a rare manuscript. Serious but not stern."
gender: male
accent: british
pitch: low
pace: slow
mood: [formal, reverent, precise, ancient]
shelves: [SPIRITUAL, ESOTERIC]
content_types: [reading, library]
compatible_with: [E2a, E2c, E5d]
```

### V10 — The Companion
```yaml
id: V10
name: "The Companion"
persona: "Friendly, modern, relatable. Like a friend who knows interesting things."
instruct: "Warm, casual male voice. Friendly, approachable. American accent. Like someone you'd want to have tea with. Not too formal, not too casual."
gender: male
accent: american
pitch: medium
pace: measured
mood: [friendly, casual, relatable, warm]
shelves: [MIND, STORY, FRESH]
content_types: [essay, daily, reading]
compatible_with: [E5a, E5b, E6a, E2a]
```

---

## Voice Compatibility Matrix

| Voice | E1a | E1b | E1c | E2a | E2c | E3a | E3b | E4a | E4b | E5a | E5b | E5c | E5d | E5e | E6a |
|-------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| V01 Sage | | | | ✅ | ✅ | ✅ | | | | ✅ | | | | | |
| V02 Storyteller | | ✅ | | ✅ | ✅ | | | | | ✅ | | | | | |
| V03 Lecturer | | | | | | | | | | ✅ | ✅ | ✅ | ✅ | | |
| V04 Mystic | | | | ✅ | | ✅ | ✅ | | | | | | | | |
| V05 Healer | | | | ✅ | | | | | | ✅ | | | | | ✅ |
| V06 Philosopher | | | | ✅ | ✅ | | | | | ✅ | | | | | |
| V07 Navigator | | | | | | | | | | ✅ | | ✅ | ✅ | ✅ | |
| V08 Dreamer | | | | ✅ | | ✅ | ✅ | | | | | | | | |
| V09 Archivist | | | | ✅ | ✅ | | | | | | | | ✅ | | |
| V10 Companion | | | | ✅ | | | | | | ✅ | ✅ | | | | ✅ |

---

## Voice Stats Schema

```yaml
voice_stats:
  voice_id: V01
  total_videos: 0
  total_watch_time_hours: 0
  avg_watch_time_minutes: 0
  avg_retention_rate: 0.0
  total_subscriber_growth: 0
  total_views: 0
  avg_views_per_video: 0
  best_performing_video: null
  worst_performing_video: null
  videos_by_shelf:
    SPIRITUAL: 0
    ESOTERIC: 0
    STORY: 0
    MIND: 0
    MUSIC: 0
    PLACE: 0
    FRESH: 0
  videos_by_engine:
    E2a: 0
    E2c: 0
    E3a: 0
    E5a: 0
    E5b: 0
    E5c: 0
    E5d: 0
    E5e: 0
    E6a: 0
  daily_metrics:
    - date: 2026-09-26
      videos: 0
      views: 0
      watch_time_hours: 0
      retention_rate: 0.0
      subscriber_growth: 0
```

---

## JEV Voice Selection Primitive

```json
{
  "at": "voice-pick",
  "primitive": "choice",
  "question": "Which voice narrates this content?",
  "criteria": {
    "V01_Sage": "SPIRITUAL/ESOTERIC reading, wise authoritative tone",
    "V02_Storyteller": "STORY reading, warm fireside narration",
    "V03_Lecturer": "MIND essay/reference, clear technical tone",
    "V04_Mystic": "ESOTERIC journey, deep mysterious tone",
    "V05_Healer": "FRESH daily, warm caring tone",
    "V06_Philosopher": "ESOTERIC/MIND essay, contemplative tone",
    "V07_Navigator": "STORY/MIND reference, steady guiding tone",
    "V08_Dreamer": "SPIRITUAL journey, ethereal dreamy tone",
    "V09_Archivist": "SPIRITUAL/ESOTERIC library, formal reverent tone",
    "V10_Companion": "MIND/STORY/FRESH essay, friendly casual tone",
    "other": "none fit — human decides"
  },
  "gates": {
    "auto": 0.75
  }
}
```
