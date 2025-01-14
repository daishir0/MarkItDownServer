<?php

class MarkItDownClient {
    private $apiUrl;
    private $apiKey;

    public function __construct(string $apiUrl, string $apiKey) {
        $this->apiUrl = rtrim($apiUrl, '/');
        $this->apiKey = $apiKey;
    }

    /**
     * ファイルをMarkdownに変換
     * 
     * @param string $filePath 変換するファイルのパス
     * @return array 変換結果（'markdown' => 変換されたテキスト, 'cached' => キャッシュ使用有無）
     * @throws Exception 変換失敗時
     */
    public function convertToMarkdown(string $filePath): array {
        if (!file_exists($filePath)) {
            throw new Exception("File not found: {$filePath}");
        }

        $curl = curl_init();
        $postFields = [
            'file' => new CURLFile($filePath)
        ];

        curl_setopt_array($curl, [
            CURLOPT_URL => $this->apiUrl . '/convert',
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => $postFields,
            CURLOPT_HTTPHEADER => [
                'X-API-Key: ' . $this->apiKey,
                'Accept: application/json'
            ]
        ]);

        $response = curl_exec($curl);
        $httpCode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
        
        if ($error = curl_error($curl)) {
            curl_close($curl);
            throw new Exception("API request failed: {$error}");
        }
        
        curl_close($curl);

        if ($httpCode !== 200) {
            throw new Exception("API returned error code: {$httpCode}");
        }

        $result = json_decode($response, true);
        if (json_last_error() !== JSON_ERROR_NONE) {
            throw new Exception("Failed to parse API response");
        }

        return $result;
    }

    /**
     * APIサーバーの健康状態をチェック
     * 
     * @return bool サーバーが正常に動作しているかどうか
     */
    public function checkHealth(): bool {
        $curl = curl_init();
        
        curl_setopt_array($curl, [
            CURLOPT_URL => $this->apiUrl . '/health',
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_HTTPHEADER => [
                'X-API-Key: ' . $this->apiKey,
                'Accept: application/json'
            ]
        ]);

        $response = curl_exec($curl);
        $httpCode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
        
        curl_close($curl);

        if ($httpCode !== 200) {
            return false;
        }

        $result = json_decode($response, true);
        return isset($result['status']) && $result['status'] === 'healthy';
    }
}

// 使用例
try {
    $client = new MarkItDownClient(
        'http://localhost:8000',  // APIサーバーのURL
        'your_secure_api_key_here'  // APIキー
    );

    // サーバーの健康状態をチェック
    if (!$client->checkHealth()) {
        die("API server is not responding correctly\n");
    }

    // ファイルを変換
    $result = $client->convertToMarkdown('/path/to/your/document.docx');
    
    echo "Conversion successful!\n";
    echo "Cached: " . ($result['cached'] ? 'Yes' : 'No') . "\n";
    echo "Markdown content:\n" . $result['markdown'] . "\n";

} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
}