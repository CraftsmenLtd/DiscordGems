const nacl = require('tweetnacl');

exports.isVerified = (event)=> {
  const PUBLIC_KEY = process.env.PUBLIC_KEY;
  const signature = event?.headers['x-signature-ed25519']
  const timestamp = event?.headers['x-signature-timestamp'];
  const strBody = event?.body; 

  return nacl.sign.detached.verify(
    Buffer.from(timestamp + strBody),
    Buffer.from(signature, 'hex'),
    Buffer.from(PUBLIC_KEY, 'hex')
  );
};