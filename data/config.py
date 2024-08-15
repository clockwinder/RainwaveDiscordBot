class botChannels:
    restrictVoiceChannels = False
    allowedVoiceChannels = []
    restrictTextChannels = False
    allowedTextChannels = []

# Checks to see if override_botChannels exists in the private.py file
# If it does, it imports the override_botChannels function to set channel restrictions
try:
    from private.private import override_botChannels
    override_botChannels(botChannels)
except ImportError:
    pass