import discord
from datetime import datetime
import pandas as pd

presence_logs = []

def setup_presence_logging(bot):
    @bot.event
    async def on_voice_state_update(member, before, after):
        """Logs when members join, leave, or switch voice channels."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if before.channel is None and after.channel is not None:
            log = {
                "Member": str(member), 
                "Action": "Joined", 
                "Channel": after.channel.name, 
                "Time": timestamp
            }
            print(log)
            presence_logs.append(log)

        elif before.channel is not None and after.channel is None:
            log = {
                "Member": str(member), 
                "Action": "Left", 
                "Channel": before.channel.name, 
                "Time": timestamp
            }
            print(log)
            presence_logs.append(log)

        elif before.channel is not None and after.channel is not None and before.channel != after.channel:
            left_log = {
                "Member": str(member), 
                "Action": "Left", 
                "Channel": before.channel.name, 
                "Time": timestamp
            }
            joined_log = {
                "Member": str(member), 
                "Action": "Joined", 
                "Channel": after.channel.name, 
                "Time": timestamp
            }
            print(left_log)
            print(joined_log)
            presence_logs.extend([left_log, joined_log])

        if presence_logs:
            df = pd.DataFrame(presence_logs)
            df.to_csv("presence.csv", index=False)
