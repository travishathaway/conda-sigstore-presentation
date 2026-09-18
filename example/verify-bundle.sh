#! /bin/bash

cat <<EOF
cosign verify-blob
    --bundle test.bundle.json
    --certificate-oidc-issuer https://github.com/login/oauth
    --certificate-identity travis.j.hathaway@gmail.com
    test.txt

EOF

read -p "Press Enter to continue" </dev/tty

cosign verify-blob \
    --bundle test.bundle.json \
    --certificate-oidc-issuer https://github.com/login/oauth \
    --certificate-identity travis.j.hathaway@gmail.com \
    'test.txt'
