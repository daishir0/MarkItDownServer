## Overview
MarkItDownServer is a FastAPI-based server application that converts various document formats (PDF, DOCX, ODT, etc.) to Markdown format. It features API key authentication, file caching, and health monitoring capabilities.

## Installation
1. Clone the repository:
```bash
git clone https://github.com/daishir0/MarkItDownServer.git
cd MarkItDownServer
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create required directories:
```bash
mkdir uploads cache logs
```

5. Copy and configure settings:
```bash
cp config.sample.py config.py
```
Edit `config.py` to set your API key and other configurations.

The directory structure should look like this:
```
MarkItDownServer/
├── main.py
├── config.py
├── requirements.txt
├── uploads/        # For temporary file uploads
├── cache/         # For caching converted files
└── logs/          # For log files

## Usage
1. Start the server:
```bash
python main.py
```
The server will run on `http://localhost:8000`

2. API Endpoints:
- POST `/convert`: Convert document to Markdown
- GET `/health`: Check server health status

3. Example using PHP client:
```php
$client = new MarkItDownClient(
    'http://localhost:8000',
    'your_secure_api_key_here'
);
$result = $client->convertToMarkdown('/path/to/your/document.docx');
```

## Notes
- Supported file formats: DOC, DOCX, PDF, TXT, RTF, ODT, ODS, ODP, ODG, ODF, HTML, XML
- Maximum file size: 10MB (configurable)
- Implements file caching to improve performance
- Requires valid API key for all operations except health check

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---

# MarkItDownServer
## 概要
MarkItDownServerは、さまざまな文書形式（PDF、DOCX、ODTなど）をMarkdown形式に変換するFastAPIベースのサーバーアプリケーションです。APIキー認証、ファイルキャッシュ、ヘルスモニタリング機能を備えています。

## インストール方法
1. リポジトリをクローンします：
```bash
git clone https://github.com/daishir0/MarkItDownServer.git
cd MarkItDownServer
```

2. 仮想環境を作成して有効化します：
```bash
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
```

3. 必要なパッケージをインストールします：
```bash
pip install -r requirements.txt
```

4. 必要なディレクトリを作成します：
```bash
mkdir uploads cache logs
```

5. 設定をコピーして構成します：
```bash
cp config.sample.py config.py
```
`config.py`を編集してAPIキーやその他の設定を行います。

ディレクトリ構造は以下のようになります：
```
MarkItDownServer/
├── main.py
├── config.py
├── requirements.txt
├── uploads/        # 一時的なファイルアップロード用
├── cache/         # 変換済みファイルのキャッシュ用
└── logs/          # ログファイル用

## 使い方
1. サーバーを起動します：
```bash
python main.py
```
サーバーは`http://localhost:8000`で実行されます

2. APIエンドポイント：
- POST `/convert`：文書をMarkdownに変換
- GET `/health`：サーバーの健康状態を確認

3. PHPクライアントの使用例：
```php
$client = new MarkItDownClient(
    'http://localhost:8000',
    'your_secure_api_key_here'
);
$result = $client->convertToMarkdown('/path/to/your/document.docx');
```

## 注意点
- 対応ファイル形式：DOC、DOCX、PDF、TXT、RTF、ODT、ODS、ODP、ODG、ODF、HTML、XML
- 最大ファイルサイズ：10MB（設定可能）
- パフォーマンス向上のためのファイルキャッシュ機能を実装
- ヘルスチェックを除くすべての操作に有効なAPIキーが必要
