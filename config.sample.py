import os
import logging

# API設定
API_KEY = "your-api-key"

# ディレクトリ設定
UPLOAD_DIR = "uploads"
CACHE_DIR = "cache"
LOGS_DIR = "logs"

# ファイルサイズ制限（バイト単位）
MAX_FILE_SIZE = 10485760  # 10MB

# ファイル保持設定
KEEP_UPLOADED_FILES = True  # デフォルトでファイルを保持

# アップロード可能なファイル形式
ALLOWED_EXTENSIONS = {
    'doc', 'docx', 'pdf', 'txt', 'rtf',
    'odt', 'ods', 'odp', 'odg', 'odf',
    'htm', 'html', 'xml'
}

# ロギング設定
LOG_FILE = os.path.join(LOGS_DIR, "markitdown_server.log")
logging.basicConfig(
    filename=LOG_FILE, 
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
LOGGER = logging.getLogger(__name__)

def is_allowed_file(filename: str) -> bool:
    """
    ファイルの拡張子が許可されているかチェックする
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS