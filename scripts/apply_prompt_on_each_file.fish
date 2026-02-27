#!/usr/bin/env fish
# This script applies a prompt to each laws

set MODEL "google/gemini-3-flash-preview"

set -l counter 1
set -l total (count (find content/textes/ -name '*.md' -and ! -name '_index.md'))

for FILENAME in (find content/textes/ -name '*.md' -and ! -name '_index.md')
    set FILE (basename $FILENAME)
    set DIR (dirname $FILENAME)

    if test $counter -le 48
        echo -e "\033[1mSkipping file $counter of $total: $FILENAME\033[0m"
        set counter (math $counter + 1)
        continue
    end

    echo -e "\033[1mProcessing file $counter of $total: $FILENAME\033[0m"
    opencode run --model $MODEL --file $FILE --dir $DIR $argv

    set counter (math $counter + 1)
end
