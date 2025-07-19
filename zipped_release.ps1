# バージョン番号が記載されたファイルのパス
$versionFilePath = "essential_brush_saver\blender_manifest.toml"

# ファイルの内容を行単位で読み込み
$lines = Get-Content $versionFilePath

# 行単位で処理
foreach ($line in $lines) {
    if ($line -match '^version\s*=\s*"(.*?)"$') {

        # バージョン番号を取得
        Write-Output "抽出したバージョン: $($matches[1])"
        $version = $matches[1]

        # ZIPファイルの保存先およびファイル名を生成
        $zipFileName = "essential_brush_saver-$version.zip"

        # 圧縮対象のフォルダー
        $sourceFolder = "essential_brush_saver\*"

        # 圧縮を実行
        Compress-Archive -Force -Path $sourceFolder -DestinationPath $zipFileName

        # 成功メッセージを出力
        Write-Output "圧縮が成功しました: $zipFileName"
        break
    }
}

# バージョン番号の抽出に失敗した場合のエラーメッセージ
if (-not $version) {
    Write-Error "version.txt からバージョン番号を抽出できませんでした。ファイルの内容: $($lines -join "`n")"
}