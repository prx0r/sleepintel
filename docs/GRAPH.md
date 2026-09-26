# GRAPH — engines as roots, channels as variations (v2, 2026-09-26)

238 nodes no longer fit a node map — engines and shelves are the graph now.
Full membership: registry/channels.yaml (validated). Detail maps per
engine live in SUBENGINES.md.

```mermaid
graph TD
  E1[HOSTED-MUSIC · 20] --> MUSIC[MUSIC shelf · 20]
  E2[READING · 62] --> SPIRITUAL[SPIRITUAL · 19]
  E2 --> ESOTERICa[ESOTERIC · 14]
  E2 --> STORYa[STORY · 90]
  E3[GUIDED · 5] --> SPIRITUAL
  E4[AMBIENCE · 4] --> PLACE[PLACE · 4]
  E5[TALK · 152] --> STORYa
  E5 --> MIND[MIND · 90]
  E5 --> ESOTERICa
  E6[FRESHNESS · 1] --> FRESH[FRESH · 1]
```

Counts: E1·20 E2·62 E3·5 E4·4 E5·152 E6·1. Shelves: Spiritual·19
Esoteric·14 Story·90 Mind·90 Music·20 Place·4 Fresh·1. Splits intentional.
