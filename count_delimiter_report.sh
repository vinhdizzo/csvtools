#! /usr/bin/env bash

export raw_dir=
export dlm='|'
export report_only_nonperfects=1 ## 1: nonperfects; 0: all
extension=csv
njobs=4

function count_delimiter {
    # echo "Counting delimiter: $1 ..." >&2
    tempfile=/tmp/tmp-$(od -N4 -tu /dev/random | awk 'NR==1 {print $2} {}')
    cat "$1" | sed "s/[^$dlm]//g" | awk "{ print length }" | sort | uniq -c > $tempfile
    if [ $report_only_nonperfects -eq 0 ]; then
        echo "Counting delimiter: $1 ..."
        cat $tempfile
    else
        if [ `wc -l < $tempfile` -gt 1 ]; then
            echo "Counting delimiter: $1 ..."
            cat $tempfile
        fi
    fi
    rm $tempfile
}
export -f count_delimiter

ls $raw_dir/*.$extension | parallel --no-notice -j $njobs count_delimiter
