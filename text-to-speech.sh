# !/bin/sh
# echo $_
say -v ${1} ${2} -o ${3}.aiff
lame --decode "${3}.aiff" "${3}.wav" --quiet && rm "${3}.aiff"