from google import genai

client = genai.Client(
    vertexai=True,
    project="eni-gdemos-aiagent",
    location="global",
)

response = client.agents.delete(id="AGENT_ID")
print(response)