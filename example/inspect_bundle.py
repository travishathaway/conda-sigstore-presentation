# /// script
# requires-python = ">=3.11"
# dependencies = ["sigstore"]
#
# [tool.pixi.workspace]
# channels = ["conda-forge"]
#
# [tool.pixi.dependencies]
# sigstore = "*"
# ///

import json
import sys
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from sigstore.models import Bundle


SIGSTORE_OIDS = {
    # Legacy GitHub-specific extensions
    "1.3.6.1.4.1.57264.1.1": "oidc_issuer_legacy",
    "1.3.6.1.4.1.57264.1.2": "github_workflow_trigger_legacy",
    "1.3.6.1.4.1.57264.1.3": "github_workflow_sha_legacy",
    "1.3.6.1.4.1.57264.1.4": "github_workflow_name_legacy",
    "1.3.6.1.4.1.57264.1.5": "github_workflow_repository_legacy",
    "1.3.6.1.4.1.57264.1.6": "github_workflow_ref_legacy",

    # Current provider-neutral extensions
    "1.3.6.1.4.1.57264.1.8": "oidc_issuer",
    "1.3.6.1.4.1.57264.1.9": "build_signer_uri",
    "1.3.6.1.4.1.57264.1.10": "build_signer_digest",
    "1.3.6.1.4.1.57264.1.11": "runner_environment",
    "1.3.6.1.4.1.57264.1.12": "source_repository_uri",
    "1.3.6.1.4.1.57264.1.13": "source_repository_digest",
    "1.3.6.1.4.1.57264.1.14": "source_repository_ref",
    "1.3.6.1.4.1.57264.1.15": "source_repository_identifier",
    "1.3.6.1.4.1.57264.1.16": "source_repository_owner_uri",
    "1.3.6.1.4.1.57264.1.17": "source_repository_owner_identifier",
    "1.3.6.1.4.1.57264.1.18": "build_config_uri",
    "1.3.6.1.4.1.57264.1.19": "build_config_digest",
    "1.3.6.1.4.1.57264.1.20": "build_trigger",
    "1.3.6.1.4.1.57264.1.21": "run_invocation_uri",
    "1.3.6.1.4.1.57264.1.22": "source_repository_visibility",
    "1.3.6.1.4.1.57264.1.23": "deployment_environment",
    "1.3.6.1.4.1.57264.1.24": "token_subject",
}


def decode_der_string(data: bytes) -> str:
    """Decode the DER UTF8String/IA5String used by modern Fulcio OIDs."""
    if len(data) < 2:
        return data.hex()

    tag = data[0]
    first_length = data[1]
    offset = 2

    if first_length & 0x80:
        length_bytes = first_length & 0x7F
        if len(data) < offset + length_bytes:
            return data.hex()
        length = int.from_bytes(data[offset : offset + length_bytes], "big")
        offset += length_bytes
    else:
        length = first_length

    value = data[offset : offset + length]
    encoding = {
        0x0C: "utf-8",      # UTF8String
        0x16: "ascii",      # IA5String
        0x13: "ascii",      # PrintableString
        0x1E: "utf-16-be",  # BMPString
    }.get(tag)

    if encoding is None:
        return data.hex()

    try:
        return value.decode(encoding)
    except UnicodeDecodeError:
        return data.hex()


def decode_extension(oid: str, data: bytes) -> str:
    # Fulcio OIDs .1 through .6 used unwrapped raw strings.
    try:
        suffix = int(oid.rsplit(".", 1)[1])
    except ValueError:
        suffix = -1

    if 1 <= suffix <= 6:
        try:
            return data.decode()
        except UnicodeDecodeError:
            return data.hex()

    return decode_der_string(data)


def json_values(text: str):
    """Accept ordinary JSON or concatenated/JSON-lines objects."""
    decoder = json.JSONDecoder()
    offset = 0

    while offset < len(text):
        while offset < len(text) and text[offset].isspace():
            offset += 1
        if offset >= len(text):
            return

        value, offset = decoder.raw_decode(text, offset)
        yield value


def find_bundle_objects(value):
    """Find bundles inside a Prefix wrapper, array, or JSON-lines document."""
    if isinstance(value, dict):
        if (
            "verificationMaterial" in value
            and ("dsseEnvelope" in value or "messageSignature" in value)
        ):
            yield value
            return

        for child in value.values():
            yield from find_bundle_objects(child)

    elif isinstance(value, list):
        for child in value:
            yield from find_bundle_objects(child)


def inspect_certificate(cert: x509.Certificate):
    sans = []

    try:
        san = cert.extensions.get_extension_for_class(
            x509.SubjectAlternativeName
        ).value

        for name in san:
            if isinstance(name, x509.OtherName):
                value = decode_der_string(name.value)
            else:
                value = str(name.value)

            sans.append({
                "type": type(name).__name__,
                "value": value,
            })
    except x509.ExtensionNotFound:
        pass

    claims = {}
    unknown_extensions = {}

    for extension in cert.extensions:
        if not isinstance(extension.value, x509.UnrecognizedExtension):
            continue

        oid = extension.oid.dotted_string
        raw = extension.value.value

        if oid in SIGSTORE_OIDS:
            claims[SIGSTORE_OIDS[oid]] = decode_extension(oid, raw)
        else:
            unknown_extensions[oid] = raw.hex()

    return {
        "subject": cert.subject.rfc4514_string(),
        "certificate_issuer": cert.issuer.rfc4514_string(),
        "serial_number": str(cert.serial_number),
        "not_valid_before": cert.not_valid_before_utc.isoformat(),
        "not_valid_after": cert.not_valid_after_utc.isoformat(),
        "sha256_fingerprint": cert.fingerprint(hashes.SHA256()).hex(),
        "subject_alternative_names": sans,
        "sigstore_oidc_claims": claims,
        "other_unrecognized_extensions": unknown_extensions,
    }


raw = Path(sys.argv[1]).read_text()
bundle_dicts = [
    bundle
    for value in json_values(raw)
    for bundle in find_bundle_objects(value)
]

if not bundle_dicts:
    raise SystemExit("No Sigstore bundle found")

for index, bundle_dict in enumerate(bundle_dicts):
    bundle = Bundle.from_json(json.dumps(bundle_dict))

    result = {
        "bundle_index": index,
        "media_type": bundle_dict.get("mediaType"),
        "certificate": inspect_certificate(bundle.signing_certificate),
    }

    print(json.dumps(result, indent=2))
