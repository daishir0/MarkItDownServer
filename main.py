import hashlib
import os
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Header
from fastapi.responses import JSONResponse
import shutil
from markitdown import MarkItDown
from config import (
    API_KEY, UPLOAD_DIR, CACHE_DIR, LOGS_DIR,
    MAX_FILE_SIZE, is_allowed_file, LOGGER,
    KEEP_UPLOADED_FILES
)

app = FastAPI(title="MarkItDown API Server")
markitdown = MarkItDown()

def verify_api_key(api_key: str = Header(..., alias="X-API-Key")) -> None:
    """APIキーの検証"""
    try:
        if api_key != API_KEY:
            LOGGER.warning(f"無効なAPIキーでのアクセス試行: {api_key}")
            raise HTTPException(
                status_code=403,
                detail="Invalid API key"
            )
        LOGGER.info("APIキー認証成功")
    except Exception as e:
        LOGGER.error(f"APIキー認証中にエラー発生: {str(e)}")
        raise

def calculate_file_hash(file_path: str) -> str:
    """ファイルのSHA256ハッシュ値を計算"""
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        file_hash = sha256_hash.hexdigest()
        LOGGER.info(f"ファイルハッシュ計算完了: {file_hash}")
        return file_hash
    except Exception as e:
        LOGGER.error(f"ファイルハッシュ計算中にエラー発生: {str(e)}")
        raise

def get_cached_markdown(file_hash: str) -> Optional[str]:
    """キャッシュされたMarkdownを取得"""
    try:
        cache_path = os.path.join(CACHE_DIR, f"{file_hash}.md")
        if os.path.exists(cache_path):
            with open(cache_path, 'r', encoding='utf-8') as f:
                cached_content = f.read()
                LOGGER.info(f"キャッシュからMarkdownを取得: {file_hash}")
                return cached_content
        LOGGER.info(f"キャッシュにMarkdownが見つかりません: {file_hash}")
        return None
    except Exception as e:
        LOGGER.error(f"キャッシュ取得中にエラー発生: {str(e)}")
        raise

def save_to_cache(file_hash: str, markdown_content: str) -> None:
    """Markdownをキャッシュに保存"""
    try:
        cache_path = os.path.join(CACHE_DIR, f"{file_hash}.md")
        with open(cache_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        LOGGER.info(f"Markdownをキャッシュに保存: {file_hash}")
    except Exception as e:
        LOGGER.error(f"キャッシュ保存中にエラー発生: {str(e)}")
        raise

@app.post("/convert")
async def convert_to_markdown(
    file: UploadFile = File(...),
    api_key: str = Header(..., alias="X-API-Key")
):
    """ファイルをMarkdownに変換するエンドポイント"""
    temp_file_path = None
    try:
        # APIキーの検証
        verify_api_key(api_key)
        LOGGER.info(f"ファイル変換リクエスト: {file.filename}")

        # ファイル形式の検証
        if not is_allowed_file(file.filename):
            LOGGER.warning(f"許可されていないファイル形式: {file.filename}")
            raise HTTPException(
                status_code=400,
                detail="これは変換できないファイルです"
            )

        # 一時ファイルとしてアップロード
        temp_file_path = os.path.join(os.getcwd(), UPLOAD_DIR, file.filename)
        with open(temp_file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        LOGGER.info(f"一時ファイル作成: {temp_file_path}")

        # ファイルサイズの検証
        if os.path.getsize(temp_file_path) > MAX_FILE_SIZE:
            LOGGER.warning(f"ファイルサイズ超過: {file.filename}")
            # ファイルサイズが大きすぎる場合でも、ファイルを削除せずに処理を続行
            pass

        # ファイルハッシュの計算
        file_hash = calculate_file_hash(temp_file_path)

        # キャッシュの確認
        cached_markdown = get_cached_markdown(file_hash)
        if cached_markdown:
            if not KEEP_UPLOADED_FILES:
                os.remove(temp_file_path)
            return JSONResponse(content={
                "markdown": cached_markdown,
                "cached": True
            })

        # MarkItDownを使用してMarkdownに変換（全ページ抽出のオプションを追加）
        try:
            result = markitdown.convert_local(
                temp_file_path, 
                pdf_options={
                    'check_extractable': False,
                    'ignore_metadata_extraction_restrictions': True,
                    'extract_all_pages': True,  # 全ページ抽出を強制
                    'max_pages': 9999,  # 大きな値で全ページ抽出を保証
                }
            )
            markdown_content = result.text_content
            LOGGER.info(f"ファイル変換成功: {file.filename}")
        except Exception as conversion_error:
            LOGGER.error(f"ファイル変換エラー: {str(conversion_error)}")
            raise HTTPException(
                status_code=500,
                detail="これは変換できないファイルです"
            )

        # キャッシュに保存
        save_to_cache(file_hash, markdown_content)

        # 一時ファイルの削除
        if not KEEP_UPLOADED_FILES:
            os.remove(temp_file_path)

        return JSONResponse(content={
            "markdown": markdown_content,
            "cached": False
        })

    except HTTPException as http_err:
        LOGGER.error(f"HTTPエラー: {http_err.detail}")
        raise
    except Exception as e:
        LOGGER.error(f"予期せぬエラー発生: {str(e)}")
        if temp_file_path and os.path.exists(temp_file_path):
            if not KEEP_UPLOADED_FILES:
                os.remove(temp_file_path)
        raise HTTPException(
            status_code=500,
            detail="これは変換できないファイルです"
        )

@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    LOGGER.info("ヘルスチェック実行")
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    # 必要なディレクトリの作成
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)
    # サーバーの起動
    LOGGER.info("MarkItDownサーバー起動")
    uvicorn.run(app, host="0.0.0.0", port=8000)