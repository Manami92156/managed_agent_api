from google import genai

client = genai.Client(
    vertexai=True,
    project="eni-gdemos-aiagent",
    location="global",
)

stream = client.interactions.create(
    agent="agent-api-test",
    input="Tell me the name of python packages used for data analysis.",
    stream=True,
    background=True,
    store=True,
)

for event in stream:
    print(event)