import os

# API設定
API_KEY = "your-api-key"

# ディレクトリ設定
UPLOAD_DIR = "uploads"
CACHE_DIR = "cache"

# ファイルサイズ制限（バイト単位）
MAX_FILE_SIZE = 10485760  # 10MB

# アップロード可能なファイル形式
ALLOWED_EXTENSIONS = {
    'doc', 'docx', 'pdf', 'txt', 'rtf',
    'odt', 'ods', 'odp', 'odg', 'odf',
    'htm', 'html', 'xml'
}

def is_allowed_file(filename: str) -> bool:
    """
    ファイルの拡張子が許可されているかチェックする
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS