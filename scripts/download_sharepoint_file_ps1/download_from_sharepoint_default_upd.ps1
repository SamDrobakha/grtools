# usage
# set sharepoint link (from dev console find in GET request)
# set cookies (from dev console find in GET request and parse)
# (optional) set download and log files destination

# Define variables
$sharepointUrl = "LINK"
$tempFilePath = "C:\Users\Administrator\Downloads\download.zip"
$logFilePath = "C:\Users\Administrator\Downloads\download.log"
$sleepTime = 2  # Sleep time in seconds between retries
$chunkSize = 104857600  # 100 MB chunk size

# Define cookies extracted from Firefox
$cookies = @(
"COOKIES"
)

# Function to log messages
function Log-Message {
    param (
        [string]$message
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "$timestamp - $message"
    Add-Content -Path $logFilePath -Value $logMessage
}

# Function to download file in chunks with resume capability and retry logic using HttpClient
function Download-File {
    param (
        [string]$url,
        [string]$outputFilePath,
        [array]$cookies,
        [int]$sleepTime,
        [int]$chunkSize
    )

    $downloadSuccess = $false
    $handler = New-Object System.Net.Http.HttpClientHandler
    $handler.UseCookies = $false
    $httpClient = [System.Net.Http.HttpClient]::new($handler)

    # Add cookies to headers
    $cookieHeader = [string]::Join("; ", $cookies)
    $httpClient.DefaultRequestHeaders.Add("Cookie", $cookieHeader)
    $httpClient.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0")
    $httpClient.DefaultRequestHeaders.Add("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8")
    $httpClient.DefaultRequestHeaders.Add("Accept-Language", "en-US,en;q=0.5")
    $httpClient.DefaultRequestHeaders.Add("Accept-Encoding", "gzip, deflate, br, zstd")
    $httpClient.DefaultRequestHeaders.Add("Connection", "keep-alive")

    while (-not $downloadSuccess) {
        try {
            $resume = Test-Path $outputFilePath
            $startBytes = 0

            if ($resume) {
                $startBytes = (Get-Item $outputFilePath).Length
                Log-Message "Resuming download from $startBytes bytes."
            }

            $endBytes = $startBytes + $chunkSize - 1
            $httpClient.DefaultRequestHeaders.Remove("Range")
            $httpClient.DefaultRequestHeaders.Range = [System.Net.Http.Headers.RangeHeaderValue]::new($startBytes, $endBytes)

            Log-Message "Starting download attempt from $url (bytes $startBytes-$endBytes)."
            $response = $httpClient.GetAsync($url, [System.Net.Http.HttpCompletionOption]::ResponseHeadersRead).Result
            if ($response.StatusCode -eq [System.Net.HttpStatusCode]::Forbidden) {
                throw "Access forbidden: ensure your cookies and permissions are correct."
            }
            $response.EnsureSuccessStatusCode()

            $contentStream = $response.Content.ReadAsStreamAsync().Result
            $fileStream = [System.IO.File]::Open($outputFilePath, [System.IO.FileMode]::Append)
            $contentStream.CopyTo($fileStream)
            $contentStream.Close()
            $fileStream.Close()

            # Check if the file is fully downloaded
            if ($response.Headers.Contains("Content-Range")) {
                $contentRange = $response.Headers.GetValues("Content-Range") | Select-Object -First 1
                $totalSize = [int64]($contentRange.Split('/')[1])
            } elseif ($response.Content.Headers.ContentLength -and $startBytes -eq 0) {
                $totalSize = [int64]$response.Content.Headers.ContentLength
            } else {
                $totalSize = (Get-Item $outputFilePath).Length
            }

            if ((Get-Item $outputFilePath).Length -eq $totalSize) {
                Log-Message "Download completed successfully."
                $downloadSuccess = $true
            }

        } catch {
            $errorMessage = $_.Exception.Message
            $detailedError = $_.Exception | Format-List | Out-String
            Log-Message ("Error during download: {0}" -f $errorMessage)
            Log-Message ("Detailed error: {0}" -f $detailedError)
            Log-Message "Retrying download in $sleepTime seconds..."
            Start-Sleep -Seconds $sleepTime
        }
    }

    $httpClient.Dispose()
}

# Start the download process
try {
    Log-Message "Starting download script."
    Download-File -url $sharepointUrl -outputFilePath $tempFilePath -cookies $cookies -sleepTime $sleepTime -chunkSize $chunkSize
    Log-Message "Download script completed."
} catch {
    $errorMessage = $_.Exception.Message
    $detailedError = $_.Exception | Format-List | Out-String
    Log-Message ("Download script encountered an error: {0}" -f $errorMessage)
    Log-Message ("Detailed error: {0}" -f $detailedError)
}
