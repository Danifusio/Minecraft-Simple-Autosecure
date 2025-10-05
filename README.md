# Minecraft-OTP-Discord-Verification-Sim

## Disclaimer
**This project is intended for educational and ethical cybersecurity research only.** Any use of this software on systems, services, or individuals without **explicit permission** is strictly prohibited and may be illegal. It is the end user's responsibility to comply with all applicable laws and platform policies. The authors assume no liability for any misuse or consequences.

## What Does It Do?

This project demonstrates how Discord bots can be used to **simulate social engineering techniques**, such as impersonating account verification flows for platforms like Minecraft. It is designed to help developers, educators, and security professionals understand and visualize how deceptive user interfaces might trick users into sharing account information.

The bot can be configured to request a Minecraft username and email under the guise of "verification." It then simulates a login prompt through Microsoft’s authentication interface, showing how attackers might attempt to exploit trust and trick users into sharing login codes.

This simulation can be used in **closed environments** for security awareness training or ethical testing. **No real account credentials should be collected or misused.**



## How to Run

1. **Download Python**: [Download Python](https://www.python.org/downloads/release/python-3110/)
2. **Create Your Bot**:
    - Generate your bot token and grant it all intents.
3. **Get MailSlurp API For Auto Secure**:
   - Visit [MailSlurp](https://www.mailslurp.com/) and copy the API key.
4. **Get Hypixel API For Stats**(You can skip this step):
   - Visit [Hypixel Dashboard](https://developer.hypixel.net/) and register for a account.
5. **Configure the Bot**:
    - Place the token Hypixel API, MailSlurp API into `config.py`.
    - Open bot.py and add your Discord ID in the line `self.admins = [YOUR DISCORD ID]`.
6. **Install Requirements**:
    - Open Command Prompt in the project folder and run `pip install -r requirements.txt`.
7. **Run the Bot**:
    - Execute the bot with the command `python bot.py`.
8. **Sync Commands**:
    - In your Discord server, type `!sync global`.
9. **Set Up Webhook**:
    - Use `/webhook` and enter the destination for your logs.

## What It Looks Like

### Logs Interface<br>
![Logs Interface](https://i.imgur.com/7ycbJLp.png)

### CMD Interface<br>
![CMD Prompt Interface](https://i.imgur.com/Hp0rAh4.png)

### Victim's Point of View<br>
(The profile picture of your bot may differ)<br>
![Victim's POV](https://i.imgur.com/s91N2fp.png)


(These Images Are No Longer Accurate I Will Update Soon)
