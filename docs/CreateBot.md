# Create Discord Bot

- Log in to discord from a web browser and open https://discord.com/developers/applications
- Click on "New Application" button from "Discord Developer Portal".
<p align="center">
  <img src="resources/CreateBot/New%20Application.png" alt="New Application">
</p>

- An Application creation dialog will be opened. Provide application name (e.g: craftsmen-app) and Team on application dialog and click on "Create" button.
<p align="center">
  <img src="resources/CreateBot/Create%20Application.png" alt="Create Application" width="50%">
</p>

- On next page an application will be created. Copy Application ID and Public Key and save it to somewhere. We will need it later.
<p align="center">
  <img src="resources/CreateBot/App%20Id%20and%20Public%20Key.png" alt="Application Id and Public Key">
</p>

- From left menu, click on "Bot".
<p align="center">
  <img src="resources/CreateBot/Bot%20Menu.png" alt="Bot Menu" width="50%">
</p>

- A page will be appeared to add bot.
<p align="center">
  <img src="resources/CreateBot/Add%20Bot.png" alt="Add Bot">
</p>

- Click on "Add Bot" button. A dialog will be opened to proceed to add the bot. After proceeding a bot will be created. Note that you may need to apply 2FA with this procedure.
- After adding bot, copy the bot token and save it along with Application ID and Public Key that you have already saved. We will need these later.
Note that if you can not copy bot token within short time the "Copy" and "View Token" button will disappear. Then reset the bot token and copy it. You may need 2FA verification while resetting bot token.
<p align="center">
  <img src="resources/CreateBot/Copy%20Token.png" alt="Copy Token">
</p>

- At the bottom of bot page, look for "MESSAGE CONTENT INTENT". Once found, turn it on and click "Save Changes" button.
<p align="center">
  <img src="resources/CreateBot/Message%20Content%20Intent.png" alt="Message Content Intent">
</p>

- Then click on "OAuth2" menu from left menu pan and click "URL Generator" sub-menu.
- From "SCOPES", check "bot".
<p align="center">
  <img src="resources/CreateBot/Scopes.png" alt="Application Scopes">
</p>

- From "BOT PERMISSIONS", check "Send messages".
<p align="center">
  <img src="resources/CreateBot/Bot%20Permissions.png" alt="Application Bot Permissions">
</p>

- Then from "GENERATED URL", copy the url.
<p align="center">
  <img src="resources/CreateBot/Generated%20URL.png" alt="Generated URL">
</p>

- Paste the url to another browser tab and hit "Enter". A dialog will be opened to add bot to your server. Selected your server from server dropdown list and click "Continue".
<p align="center">
  <img src="resources/CreateBot/Add%20Bot%20to%20Server.png" alt="Add Bot to Server" width="50%">
</p>

- Close the browser tab after adding the bot to your server. You're done.
