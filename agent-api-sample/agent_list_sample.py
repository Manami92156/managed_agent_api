from google import genai

# クライアントの初期化（先ほどと同じプロジェクトを指定）
client = genai.Client(
    vertexai=True,
    project="eni-gdemos-aiagent",  # 先ほど成功したプロジェクトIDに変えてください
    location="global",
)

print("🔍 作成済みのマネージド エージェントを一覧表示します...")

response = client.agents.list()
# プロジェクト内のエージェントをリストアップ
for agent in response.agents:
    print("-" * 40)
    print(f"{agent}")
    # print(f"🔹 エージェントID: {agent.id}")
    # print(f"🔹 表示名（リソース名）: {agent.name}")
    # print(f"🔹 説明: {agent.description}")
    # print(f"🔹 モデル: {agent.base_agent}")