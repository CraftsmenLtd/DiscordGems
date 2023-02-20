const axios = require('axios').default;

const url = `https://discord.com/api/v8/applications/${process.env.APP_ID}/guilds/${process.env.GUILD_ID}/commands`

const headers = {
  "Authorization": `Bot ${process.env.BOT_TOKEN}`,
  "Content-Type": "application/json"
}

const command_data = {
  "name": "test",
  "type": 1,
  "description": "replies with hello",
}

axios.post(url, JSON.stringify(command_data), {
  headers: headers,
})
