import os
import re

html_path = r'c:\Antigravity_2026\InMedios_Mitta\Mitta_SEO_Audit_Abril.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove emojis (most common emoji ranges)
# Emoji ranges:
# U+1F600 to U+1F64F (emoticons)
# U+1F300 to U+1F5FF (symbols & pictographs)
# U+1F680 to U+1F6FF (transport & map symbols)
# U+1F700 to U+1F77F (Alchemical Symbols)
# U+1F780 to U+1F7FF (Geometric Shapes Extended)
# U+1F800 to U+1F8FF (Supplemental Arrows-C)
# U+1F900 to U+1F9FF (Supplemental Symbols and Pictographs)
# U+1FA00 to U+1FA6F (Chess Symbols)
# U+1FA70 to U+1FAFF (Symbols and Pictographs Extended-A)
# U+2600 to U+26FF (Misc symbols)
# U+2700 to U+27BF (Dingbats)
# Let's use a regex to match characters > U+2000 that aren't common punctuation or letters.
# A simpler way is to just use the emoji library, but since it might not be installed,
# we'll use a broad unicode regex for emojis.
emoji_pattern = re.compile(r'[\U00010000-\U0010ffff\u2600-\u26FF\u2700-\u27BF]', flags=re.UNICODE)

cleaned_content = emoji_pattern.sub('', content)

# There are also some common text-based emojis or specific ones like 🤖 📊 📉 📈 🔍 ⚙️ 🚨 💡 ⚡ 🧠
# Let's also do a manual replace of some common icons just in case they fall outside the range
common_icons = ['🤖', '📊', '📉', '📈', '🔍', '⚙️', '🚨', '💡', '⚡', '🧠', '✅', '❌', '🚀', '🛑', '⚠️', '🎯', '📌', '🛠️', '📝', '🔗', '🌐', '📱', '💻']
for icon in common_icons:
    cleaned_content = cleaned_content.replace(icon, '')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(cleaned_content)
    
print("Cleaned HTML")
