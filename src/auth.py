import lnurl
from secp256k1 import PrivateKey
from urllib.parse import urlparse
from urllib.parse import parse_qs
from binascii import hexlify

def generatePrivateKey():
    privateKey = PrivateKey()
    privateKeySer = privateKey.serialize()
    #privateKeyHex = hexlify(privateKeySer)
    return privateKeySer

def signK1(privKeyHex, k1):
    print(f'Signing k1: {k1}')
    print(f'------------')
    privateKey = PrivateKey(bytes(bytearray.fromhex(privKeyHex)))

    pubKeyRaw = privateKey.pubkey
    pubKeySer_Comp = pubKeyRaw.serialize(compressed=True)
    pubKeyHex_Comp = hexlify(pubKeySer_Comp)
    pubKeyHex_Comp = pubKeyHex_Comp.decode('utf-8')
    print(f'Public key Serialized, Compressed, converted to hex: {pubKeyHex_Comp}')

    sig = privateKey.ecdsa_sign(bytes(bytearray.fromhex(k1)), raw=True)

    sig_ser_hex = ''.join('{:02x}'.format(x) for x in privateKey.ecdsa_serialize(sig))
    print(f'Signature Serialized, converted to hex: {sig_ser_hex}')

    return pubKeyHex_Comp,sig_ser_hex

def parseLink(link):
    link = link.replace("lightning:","",1)
    print(f'Parsing: {link}')
    url = lnurl.decode(link)
    parsed_url = urlparse(url)
    k1 = parse_qs(parsed_url.query)['k1'][0]
    host = parsed_url.hostname
    http = parsed_url.scheme # normally 'https'
    print(f'url:  {url}')
    print(f"hostname: {host}")
    print(f'k1: {k1}')
    return http, host, k1

def packLink(http, host, k1, sig, pubKey):
    url = str(f'{http}://{host}/login?k1={k1}&tag=login&sig={sig}&key={pubKey}')
    return url

if __name__ == "__main__":
    print(generatePrivateKey())