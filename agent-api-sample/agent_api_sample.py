from google import genai

client = genai.Client(
    vertexai=True,
    project="eni-gdemos-aiagent",
    location="global",
)

agent = client.agents.create(
    id="agent-api-test2",
    base_agent="antigravity-preview-05-2026",
    description="お試し作成用のagentです",
    system_instruction="""
    ユーザーの意向に沿って行動してください。
    レポートを作成した場合はツールを用いてGoogleドキュメントにしてください。
    レポートのURLも必ずユーザーに通知するようにしてください。
    """,
    tools=[
        {"type": "google_search"},
        {"type": "url_context"},
        {
            "type": "mcp_server",
            "name": "create_google_docs",
            "url" : "http://127.0.0.1:8000"
        },
    ],
    base_environment={
        "type": "remote",
        "sources": [
            {
                "type": "gcs",
                "source": "gs://agent-api-test",
                "target": "/.agent",
            }
        ],
        "network": {"allowlist": [{"domain": "*"}]},
    },
)
