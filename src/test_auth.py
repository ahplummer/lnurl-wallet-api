import unittest

from auth import parseLink, signK1, packLink

lnlink = "lightning:LNURL1DP68GURN8GHJ7E3JXUEJ6V3KXQCJ6CE595URZVPS956XVWFS95UNSVFE95UN2VF595EKZWRZ94JRSE3N9EHXWUN0DVKKVUN9V5HXZURS9AKX7EMFDCLKKVFAV4NRVDFKXFJXVEPHXF3NYCESX9NRYENRVVCRYEN9VC6NXD3HX5CKZVEEVY6KGCECXUCRVVNYVCERSDPKXPJRJEPJXYEKXWPKXGUXYCFXW3SKW0TVDANKJMSR0GH5F"
# representative URL: "https://f273-2601-c4-8100-4f90-9819-9514-3a8b-d8f3.ngrok-free.app/login?k1=ef6562dfd72c2c01f2fcc02fef536751a39a5dc87062df28460d9d213c8628ba&tag=login"
privKeyHex = "7ccca75d019dbae79ac4266501578684ee64eeb3c9212105f7a3bdc0ddb0f27e"
outLink = "https://f273-2601-c4-8100-4f90-9819-9514-3a8b-d8f3.ngrok-free.app/login?k1=ef6562dfd72c2c01f2fcc02fef536751a39a5dc87062df28460d9d213c8628ba&tag=login&sig=30440220276eaab782f3f8f04a0093bc574e51d38c9b9eaae4b7c43de42abcd8007184290220726171a62057c5c72f481ff248e97c71b821677aae65567829b8f498ac35982b&key=03e9a06e539d6bf5cf1ca5c41b59121fa3df07a338322405a312c67b6349a707e9"

class TestAuth(unittest.TestCase):
    def test_parseLink(self):
        expectedK1 = "ef6562dfd72c2c01f2fcc02fef536751a39a5dc87062df28460d9d213c8628ba"
        expectedHost = "f273-2601-c4-8100-4f90-9819-9514-3a8b-d8f3.ngrok-free.app"
        expectedHttp = "https"
        http, host, k1 = parseLink(lnlink)
        self.assertEqual(http, expectedHttp)
        self.assertEqual(host, expectedHost)
        self.assertEqual(k1, expectedK1)

    def test_k1sign(self):
        expectedSig = "30440220276eaab782f3f8f04a0093bc574e51d38c9b9eaae4b7c43de42abcd8007184290220726171a62057c5c72f481ff248e97c71b821677aae65567829b8f498ac35982b"
        expectedPublicKey = "03e9a06e539d6bf5cf1ca5c41b59121fa3df07a338322405a312c67b6349a707e9"
        _, _, k1 = parseLink(lnlink)
        pubKey, sig = signK1(privKeyHex, k1)
        self.assertEqual(sig, expectedSig)
        self.assertEqual(pubKey, expectedPublicKey)

    def test_packLink(self):
        http, host, k1 = parseLink(lnlink)
        pubKey,sig = signK1(privKeyHex, k1)
        url = packLink(http,host,k1,sig,pubKey)
        self.assertEqual(url, outLink)

if __name__ == '__main__':
    unittest.main()