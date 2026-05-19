# Novatorem — Spotify Now Playing Widget

A customized, premium Spotify "Now Playing" SVG widget for GitHub profiles, deployed on Vercel.

## Features

- **Real-time Spotify data** — Currently playing track with artist, album art
- **BPM-synced equalizer bars** — Animated bars sync to the track's tempo
- **Color extraction** — Colors from album art drive gradients and glows
- **Dark cyberpunk theme** — Neon blue accents, terminal aesthetic
- **Compact & standard modes** — `?compact=true` for smaller widget
- **Marquee text** — Long track/artist names scroll smoothly
- **Blur backgrounds** — `?background_type=blur_dark` for album art blur
- **Fallback state** — Shows recent track when nothing is playing

## Quick Start

```bash
# Clone and setup
git clone https://github.com/Inzaghii17/novatorem.git
cd novatorem
cp .env.example .env

# Fill in your Spotify credentials in .env
# Then run locally:
python start.py
```

## Deployment

See [DEPLOY.md](DEPLOY.md) for complete deployment instructions.

## Usage in README

```markdown
![Spotify](https://novatorem-inzaghii17.vercel.app/api)
```

### Parameters

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `background_color` | hex (no #) | `181414` | Background color |
| `border_color` | hex (no #) | `181414` | Border color |
| `background_type` | `color`, `blur_dark`, `blur_light` | `color` | Background mode |
| `show_status` | `true`, `false` | `false` | Show "Vibing to:" text |
| `compact` | `true`, `false` | `false` | Compact layout |

## License

MIT
