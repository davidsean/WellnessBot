import os
CHANNEL = int(os.getenv('CHANNEL_ID'))

def in_wellness_channel(func):
    async def wrapper(*args, **kwargs):
        if not args[0].channel.id == CHANNEL:
            print('ignoring command out of wellness channel')
            return wrapper
        else:
            await func(*args, **kwargs)
    return wrapper
