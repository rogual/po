import simple

url = "https://chromiumembedded.googlecode.com/" \
      "files/cef_binary_1.1180.832_windows.zip"

recipe = simple.simple('cef', 'Chromium Embedded Framework', url)
