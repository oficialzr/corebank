#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cert_dir="$project_dir/.certs"
root_cert="$cert_dir/corebank-local-root-ca.pem"
root_key="$cert_dir/corebank-local-root-ca-key.pem"
server_cert="$cert_dir/localhost.pem"
server_key="$cert_dir/localhost-key.pem"
server_request="$cert_dir/localhost.csr"
extension_file="$(mktemp)"

cleanup() {
  rm -f "$extension_file" "$server_request"
}
trap cleanup EXIT

mkdir -p "$cert_dir"

if [[ ! -f "$root_cert" || ! -f "$root_key" ]]; then
  openssl req -x509 -newkey rsa:3072 -sha256 -nodes \
    -days 3650 \
    -keyout "$root_key" \
    -out "$root_cert" \
    -subj "/CN=CoreBank Local Development CA"
fi

openssl req -newkey rsa:2048 -sha256 -nodes \
  -keyout "$server_key" \
  -out "$server_request" \
  -subj "/CN=localhost"

printf '%s\n' \
  "basicConstraints=CA:FALSE" \
  "keyUsage=digitalSignature,keyEncipherment" \
  "extendedKeyUsage=serverAuth" \
  "subjectAltName=DNS:localhost,IP:127.0.0.1,IP:::1" \
  > "$extension_file"

openssl x509 -req -sha256 \
  -days 825 \
  -in "$server_request" \
  -CA "$root_cert" \
  -CAkey "$root_key" \
  -CAcreateserial \
  -out "$server_cert" \
  -extfile "$extension_file"

chmod 600 "$root_key" "$server_key"
chmod 644 "$root_cert" "$server_cert"

printf 'Certificates created in %s\n' "$cert_dir"
printf 'Trust this local CA once: %s\n' "$root_cert"
printf 'Then open https://localhost:3443\n'
