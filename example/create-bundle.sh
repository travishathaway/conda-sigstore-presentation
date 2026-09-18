#! /bin/bash

cat <<EOF
cosign sign-blob
    --yes
    --bundle test.bundle.json
    test.txt

EOF

read -p "Press Enter to continue" </dev/tty

cosign sign-blob \
    --yes \
    --bundle test.bundle.json \
    test.txt

