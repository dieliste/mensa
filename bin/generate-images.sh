# npm install svgexport -g

# favicon
cp -f svg/icon.svg static/favicon.svg
svgexport svg/icon-rounded.svg static/favicon-16x16.png 16:16
svgexport svg/icon-rounded.svg static/favicon-32x32.png 32:32

# pwa
svgexport svg/icon.svg static/apple-touch-icon.png 192:192
svgexport svg/icon-rounded.svg static/android-chrome-192x192.png 192:192
svgexport svg/icon-rounded.svg static/android-chrome-512x512.png 512:512
