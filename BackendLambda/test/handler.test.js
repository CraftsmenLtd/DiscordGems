const { isVerified } = require('../utils/discordUtil.js');
const { handler } = require('../index');

jest.mock('../utils/discordUtil.js', () => ({
  isVerified: jest.fn(),
}));

describe('handler', () => {

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('returns 401 when request is not verified', async () => {
    isVerified.mockReturnValue(false);
    const event = {
      headers: {},
      body: {},
    };
    const response = await handler(event);
    expect(response.statusCode).toBe(401);
    expect(response.body).toEqual(JSON.stringify('invalid request signature'));
  });

  test('returns 404 when body is null or undefined', async () => {
    isVerified.mockReturnValue(true);
    const event = {
      headers: {},
      body: null,
    };
    const response = await handler(event);
    expect(response.statusCode).toBe(404);
  });

  test('returns 200 with type 1 body when request is a ping', async () => {
    isVerified.mockReturnValue(true);
    const event = {
      headers: {},
      body: JSON.stringify({ "type": 1 }),
    };
    const response = await handler(event);
    expect(response.statusCode).toBe(200);
    expect(response.body).toEqual(JSON.stringify({ "type": 1 }));
  });

  test('returns 200 with type 4 body when request is a test command', async () => {
    isVerified.mockReturnValue(true);
    const event = {
      body: JSON.stringify({
        "type": 4,
        "data": { "name": "test" }
      }, null, 2)
    };
    const response = await handler(event);
    expect(response.statusCode).toBe(200);
    expect(response.body).toEqual(JSON.stringify({
      "type": 4,
      "data": { "content": "hello from lambda" }
    }));
  });

});