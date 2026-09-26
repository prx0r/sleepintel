# STYLE — global base + channel variants (v1, 2026-09-26)

A producer reads this before generating anything. Channels vary it;
nobody breaks it.

## Global base (all channels, always)

- Canvas: black `#0B0B0E`. Line: warm white `#F5F0E6`. One accent max.
- Drawn stack: whiteboard hand (or handless), slow reveal, pencil/chalk line.
- Font: Montserrat ExtraBold (titles), same family everywhere.
- Voice: en-US-AriaNeural, -5%, -2Hz (the voice IS the logo).
- Bed: low ambient or silence. Nothing with lyrics, ever.
- Logo: wedge top-left (COMPOSER—TRACK pattern generalized:
  CHANNEL — EPISODE + position small beneath).
- Jingle: identical 5-second sting opens every video on every channel —
  same three notes, channel-timbre variant allowed. Pavlovian sleep cue:
  by the third night, the sting alone lowers shoulders. Audio queued
  (house piano render on E1).

## The first-five-seconds law (the secret)

Click → thumbnail → wedge → jingle → voice: one continuous exhale. If the
viewer doesn't feel the mindset shift by second five, the video failed
before the content started. Judge pilots on the opening, not the middle.

## Per-channel variant (registry `style:` block)

accent (hex, null = inherit base gold) · font (null = Montserrat) ·
voice (null = Aria) · bed (null = low ambient) · jingle_timbre ·
logo_note. Accents assigned at pilot; everything else inherits until
a verdict says otherwise.
