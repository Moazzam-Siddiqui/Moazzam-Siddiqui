"""Everything personal lives here. Edit this file, re-run `python scripts/render_all.py`."""

USERNAME = "Moazzam-Siddiqui"
NAME = "Moazzam Ahmad Siddiqui"
PROMPT_USER = "Moazzam"
PROMPT_HOST = "github"

# Cycled by the typing animation in header.svg
ROLES = [
    "Full Stack AI Engineer",
    "Agentic AI",
    "Generative-AI, MERN, Spring",
    "Building AI Agents with Groq, Claude SDK + Google ADK",
]

TAGLINE = "Gurgaon, IN  ·  shipping cloud-native products & AI agents"

# neofetch-style rows on info-card.svg. "{...}" placeholders are filled from live data.
INFO_ROWS = [
    ("Role", "AI Engineer"),
    ("Location", "Gurgaon, Haryana"),
    ("Cert", "Generative AI Engineer – UDEMY"),
    ("Uptime", "{uptime} on GitHub"),
    ("Langs", "{top_langs}"),
    ("Frontend", "React · Next.js · TypeScript"),
    ("Backend", "Node.js · Express · Spring · Python · MongoDB"),
    ("Cloud", "AWS Lambda · API Gateway · DynamoDB "),
    ("AI", "Claude SDK · Google ADK · LLM Agents"),
    ("Repos", "{public_repos} public  ·  {stars} stars"),
    ("Activity", "{total} contributions this year"),
    ("Streak", "{current_streak}d current  ·  {longest_streak}d best"),
]

# globe.svg: home pin + arcs to the cloud regions you ship to (lat, lon)
HOME = ("Gurgaon", 28.46, 77.03)

REGIONS = [
    ("ap-south-1", 19.08, 72.88),
    ("ap-southeast-1", 1.35, 103.82),
    ("eu-central-1", 50.11, 8.68),
    ("us-east-1", 38.95, -77.45),
    ("asia-northeast1", 35.68, 139.69),
]
# tech-sphere.svg: category -> labels (each category gets its own colour)
TECH = {
    "frontend": ["React", "Next.js", "TypeScript", "JavaScript", "Tailwind"],
    "backend": ["Node.js", "Express", "Python", "MongoDB", "REST", "Stripe"],
    "cloud": ["AWS Lambda", "API Gateway", "DynamoDB", "S3","Supabase"],
    "ai": ["Groq", "Google ADK", "AI Agents", "LLMs"],
    "tools": ["Docker", "Git", "Jenkins"],
}
