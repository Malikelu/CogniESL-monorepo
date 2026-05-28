
# Fix the middleware.ts file
filepath = "/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/CogniESL Website/middleware.ts"

with open(filepath, "r") as f:
    content = f.read()

# Replace the broken password line
# The file has: const PASSWORD=*** = (err: boolean) => {
# We want: const PASSWORD=*** = (err: boolean) => {
import re
content = re.sub(
    r'const PASSWORD="\d+" \|\| "Pass123";',
    'const PASSWORD=***,
    content
)

# Replace LOGIN with _loginHtml
content = content.replace("LOGIN(", "_loginHtml(")

with open(filepath, "w") as f:
    f.write(content)

print("Fixed")
