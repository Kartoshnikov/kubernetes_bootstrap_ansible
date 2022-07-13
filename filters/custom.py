from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from sys import version_info
from binascii import hexlify


class FilterModule(object):

    def filters(self):
        return {
            'spki_fingerprint': self.spki_fingerprint,
            "s_quote": self.surround_by_s_quote,
            "to_dict": self.to_dict
        }

    def spki_fingerprint(self, pem):
        if version_info < (3, 0):
            pem_bytes = bytes(pem)
        else:
            pem_bytes = bytes(pem, 'utf8')
        cert = x509.load_pem_x509_certificate(pem_bytes, default_backend())
        public_key = cert.public_key()
        spki = public_key.public_bytes(
            serialization.Encoding.DER,
            serialization.PublicFormat.SubjectPublicKeyInfo)
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(spki)
        hash = digest.finalize()
        return hexlify(hash).decode('ascii')

    def surround_by_s_quote(self, object):
        if type(object).__name__ in ('list', 'tuple'):
            return [ "'%s'" % i for i in object ]
        else:
            return "'%s'" % object


    def to_dict(self, object):
        object = tuple(object)
        return dict(object)

