import sys
from google import genai

client = genai.Client(vertexai=True, project="eni-gdemos-aiagent", location="global")

# エージェントの完全なリソース名
agent_resource = "projects/eni-gdemos-aiagent/locations/global/agents/agent-api-test"

print("🤖 Managed Agent プレイグラウンドへようこそ！")
print("終了するには 'exit' と入力してください。\n")

# 今回は簡易的にセッションID（スレッドIDのようなもの）を固定するか、無しで毎回新規にします
# ドキュメントに準拠して interactions.create を使います
while True:
    user_input = input("👤 あなた: ")
    if user_input.lower() == "exit":
        break

    print("🤖 エージェントが思考・ツール実行中...\n", flush=True)

    # 公式ドキュメントの通りのストリーミング呼び出し
    response_stream = client.interactions.create(
        agent="agent-api-test2",
        input=user_input,
        stream=True,
        background=True,
        store=True,
    )

    # 飛んでくるイベントからテキストだけを抜き出してリアルタイム表示
    for event in response_stream:
        event_type = getattr(event, "event_type", "")
        
        # テキストが生成された瞬間をキャッチ
        if event_type == "step.delta":
            delta = getattr(event, "delta", None)
            if delta and getattr(delta, "type", "") == "text":
                # AIの生成した文字をその場に表示
                print(delta.text, end="", flush=True)
                
        # ツールが動いたことをこっそり通知
        elif event_type == "step.start":
            step = getattr(event, "step", None)
            if step and getattr(step, "type", "") == "function_call":
                print(f"\n⚙️ [ツール実行中: {getattr(step, 'name', 'unknown')}]", flush=True)

    print("\n" + "-" * 50)