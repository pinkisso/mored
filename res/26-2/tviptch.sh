#!/bin/bash

file1="res/26-2/cnnpt.m3u8"
file2="res/26-2/tvi.m3u8"
file3="res/26-2/tviint.m3u8"
file4="res/26-2/tvific.m3u8"
file5="res/26-2/tvimai.m3u8"
file6="res/26-2/tvirea.m3u8"
file7="res/26-2/tviafr.m3u8"

for file in "$file1" "$file2" "$file3" "$file4" "$file5" "$file6" "$file7"; do
  sed -i "s#wmsAuthSign=[^&]*#wmsAuthSign=$(wget -qO- https://services.iol.pt/matrix?userId -o /dev/null)#g" "$file"
done
exit 0
