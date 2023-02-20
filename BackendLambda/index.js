const { isVerified } = require('./utils/discordUtil.js');

exports.handler = async (event) => {

  if(!isVerified(event)){
    return {
      statusCode: 401,
      body: JSON.stringify('invalid request signature'),
    };
  }
  
  const body = JSON.parse(event?.body || '{}');

  // Replying to ping 
  if (body?.type == 1) {
    return {
      statusCode: 200,
      body: JSON.stringify({ "type": 1 }),
    }
  }

  // Handle test Command
  if (body?.data?.name == 'test') {
    return {
      statusCode: 200,
      body: JSON.stringify({
        "type": 4,
        "data": { "content": "hello from lambda" }
      })
    }
  }
  
  // unhandled requests
  return {
    statusCode: 404 
  }
};