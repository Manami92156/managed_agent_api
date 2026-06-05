import os
from google import genai
from googleapiclient.discovery import build
from google.auth import default
from fastmcp import FastMCP

# 1. FastMCPサーバーの初期化
mcp_server = FastMCP(
    name="Google Drive & Docs Writer",
    on_duplicate_tools="error"
)

def get_google_credentials():
    credentials, project_id = default(
        scopes=[
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/documents"
        ]
    )
    return credentials

# 2. エージェント用ツールの定義
@mcp_server.tool()
def create_report_document(title: str, content: str) -> str:
    """
    指定されたタイトルと内容（テキスト）でGoogleドキュメントを作成し、Googleドライブに保存します。
    """
    try:
        creds = get_google_credentials()
        docs_service = build('docs', 'v1', credentials=creds)
        
        print(f"[MCP] ドキュメント「{title}」を作成中...")
        doc = docs_service.documents().create(body={'title': title}).execute()
        document_id = doc.get('documentId')
        
        requests = [{'insertText': {'location': {'index': 1}, 'text': content}}]
        docs_service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
        
        doc_url = f"https://docs.google.com/document/d/{document_id}/edit"
        return f"成功: Googleドキュメントが作成されました。\nURL: {doc_url}"
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

# 3. 起動処理（実績ベースの書き方）
if __name__ == "__main__":
    print("🚀 Cloud Run（Streamable HTTP）でMCPサーバーを起動します...")
    
    mcp_server.run(
        transport="streamable-http",  # 実績のある本番用HTTP通信モード！
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),  # デフォルトをCloud Run用の8080に
    )