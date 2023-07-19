## LNURL-auth Python Wallet example

The intent of this simple project is to put the cipher-logic of Lightning authentication into one place. Normally, a Lightning wallet would process the QR-code handshake for authentication. However, this is a simple API that allows for a private key to be passed in (with appropriate permissions), to sign the k1 challenge.

For context, I wanted to created a working example of [LUDS04](https://github.com/lnurl/luds/blob/luds/04.md).

You can use this with [Lightning Login](https://lightninglogin.live/) for testing.

### Prereqs

If you want to run this in docker, only Docker is required. Otherwise, you'll need to setup a local environment.

### Run from docker
NOTE: you'll see `users=user1:password,user2:password` with these examples. For now, this code doesn't leverage anything but hardcoded users injected into the envvars. These creds are passed along via BASIC auth on the POST to the `/authenticate` endpoint.

1. Create a .env file:
```
#!/bin/bash
export users=JBlow=JoePass;SusieQ=SuePass
```
Note: you'll likely want to come back and adjust this file.
2. Open terminal #1, change directory to this one, and then source that .env to get the envvars: `source .env`
3. Docker: `make run`. Skip the `users` if you leverage a .env file.
4. Open terminal #2, get New Private Key from the `/generateKey` endpoint:
```
curl -u SusieQ:SuePass -X GET -H "Content-Type: application/json" http://127.0.0.1:8511/generateKey 
```
4. Copy the Private Key for usage in the next few steps.
5. Navigate to [Lightning Login](https://lightninglogin.live/) in your browser for testing.
6. Attempt to login via Lightning, showing the QR code. Right-click and save the QR code "link".
7. Modify your envvars to include LNURL and privateKey:
```
#!/bin/bash
export users=JBlow:JoePass,SusieQ:SuePass
export LNURL=lightning:LNURL1DP68GURN8GHJ7E3JXUEJ6V3KXQCJ6CE595URZVPS956XVWFS95UNSVFE95UN2VF595EKZWRZ94JRSE3N9EHXWUN0DVKKVUN9V5HXZURS9AKX7EMFDCLKKVFAVV6R2D3SVGMR2VR9V33NXEP4XF3RYCFEXAJRXWRRVC6XYWP4XCCNWVNXX43NXV3NXUERSVFSXV6KGV3KXESNVC3NXSUNXVFS8QURGE3XW3SKW0TVDANKJMS75VZPQ
export PRIVATE_KEY=7ccca75d019dbae79ac4266501578684ee64eeb3c9212105f7a3bdc0ddb0f27e
```
5. Using second terminal, re-source your .env (`source .env`) to get the changes.
6. Curl the authenticate endpoint for your flask app:
```
curl -u SusieQ:SuePass -X POST -H "Content-Type: application/json" http://127.0.0.1:8511/authenticate -d '{"LNURL":"'$LNURL'","key":"'$PRIVATE_KEY'"}'
```
6. Copy the returned URL, and paste into a new tab in your browser, and press enter. If you get a 200, with "OK" in the return, you have successfully logged in.
7. Your public key (tied to the privateKey injected to the endpoint) is now registered on the site.

### Run locally
1. Clone repo into a new directory.
2. Create virtualenv: `python3 -m venv .venv`
3. Activate it: `source .venv/bin/activate`
4. Install dependencies `pip install -r requirements.txt`
5. Create .env as indicated above.
6. Use `make runlocal` instead of the docker `make run`.