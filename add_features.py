#!/usr/bin/env python3
"""Add all features to BidAssist - careful step by step"""
import re

# Read the base file
with open('/home/ccampos/.openclaw/workspace/projects/bid-assist/templates/index.html', 'r') as f:
    content = f.read()

# Add Tailwind CDN if not present
if 'tailwindcss' not in content:
    content = content.replace(
        '<link href="https://fonts.googleapis.com',
        '<script src="https://cdn.tailwindcss.com"></script>\n    <link href="https://fonts.googleapis.com'
    )

# Add FontAwesome
if 'font-awesome' not in content:
    content = content.replace(
        '</head>',
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">\n    </head>'
    )

# Save intermediate
with open('/home/ccampos/.openclaw/workspace/projects/bid-assist/templates/index.html', 'w') as f:
    f.write(content)
print("Step 1: Added CDN links")
