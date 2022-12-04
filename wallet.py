from dataclasses import dataclass
import rsa


@dataclass
class Wallet:
    public_key: str
    private_key: str
    name: str

    @property
    def public_key_string(self) -> str:
        return self.public_key.save_pkcs1().decode('utf-8').lstrip('-----BEGIN RSA PRIVATE KEY-----\n').rstrip('\n-----END RSA PRIVATE KEY-----\n').lstrip('UBLIC KEY-----').rstrip('-----END RSA PUBLIC ')


def generate_new_wallet(name: str) -> Wallet:
    ''' '''
    (pub_key, priv_key) = rsa.newkeys(512)
    return Wallet(pub_key, priv_key, name)
