# Emoji System

This folder contains the emoji system for the DisChatLM chat application.

## How to Use

1. **Add Emoji Images**: Place your emoji images (PNG, JPG, etc.) in this folder
2. **Configure Emojis**: Edit `emoji_config.json` to map emoji codes to image files
3. **Use in Chat**: Type `:emoji_code:` in your messages to display the emoji

## Example

If you have an image called `smile.png` and want to use it as `:smile:`, add this to `emoji_config.json`:
```json
{
    "smile": "smile.png"
}
```

Then in chat, type `:smile:` and it will display the smile image.

## Supported Formats

- PNG (recommended for transparency)
- JPG
- GIF
- SVG

## Image Guidelines

- Recommended size: 20x20 pixels
- Keep file sizes small for better performance
- Use transparent backgrounds for better integration

## Current Emojis

- `:smile:` - smile.png
- `:heart:` - heart.png
- `:thumbsup:` - thumbsup.png
- `:wave:` - wave.png
- `:laugh:` - laugh.png
- `:cry:` - cry.png
- `:angry:` - angry.png
- `:surprised:` - surprised.png
- `:cool:` - cool.png
- `:love:` - love.png
