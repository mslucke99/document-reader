Write-Output 'Checking for Python package.'
if ($null -eq (python --version)) {
   Write-Output 'No package for python found. Installing latest version.'
   curl https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe --output python-3.8.10-amd64.exe
   Start-Process -FilePath "./python-3.8.10-amd64.exe" -ArgumentList "/quiet","PrependPath=1" -Wait
   Remove-Item python-3.8.10-amd64.exe
   Set-Alias -Name python -Value "$env:LOCALAPPDATA\Programs\Python\Python38\python.exe"
}

Write-Output 'Verifying pip installation.'
python -m ensurepip

Write-Output 'Updating pip and pipenv.'
python -m pip install --upgrade pip --no-warn-script-location
python -m pip install --upgrade pipenv --no-warn-script-location

Write-Output 'Installing Tesseract OCR'
curl https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.1.0-elag2019.exe --output tesseract-ocr-w64-setup-v4.1.0-elag2019.exe
Start-Process -FilePath "./tesseract-ocr-w64-setup-v4.1.0-elag2019.exe" -Wait
Remove-Item tesseract-ocr-w64-setup-v4.1.0-elag2019.exe

Write-Output 'Adding Tesseract OCR to user PATH'
$path = [System.Environment]::GetEnvironmentVariable('path', [System.EnvironmentVariableTarget]::User)
$path = ((($path -split ';' | Where-Object {$_ -ne ''}) + "$env:LOCALAPPDATA\Tesseract-OCR") | Get-Unique | Sort-Object) -join ';'
[System.Environment]::SetEnvironmentVariable('path', $path, [System.EnvironmentVariableTarget]::User)

Write-Output 'Installing PyAudio'
curl https://download.lfd.uci.edu/pythonlibs/y2rycu7g/PyAudio-0.2.11-cp38-cp38-win_amd64.whl --output PyAudio-0.2.11-cp38-cp38-win_amd64.whl
python -m pip install .\PyAudio-0.2.11-cp38-cp38-win_amd64.whl
Remove-Item PyAudio-0.2.11-cp38-cp38-win_amd64.whl

Write-Output 'Creating test environment'
python -m pipenv install

Write-Output 'Downloading test database'
curl -L https://www.dropbox.com/s/r2ingd0l3zt8hxs/frozen_east_text_detection.tar.gz --output frozen_east_text_detection.tar.gz
tar -xvzf frozen_east_text_detection.tar.gz
Remove-Item frozen_east_text_detection.tar.gz
