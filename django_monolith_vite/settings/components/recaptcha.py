import os

# Recptcha configuration
RECAPTCHA_REQUIRED_SCORE = 0.5
# For V3
RECAPTCHA_PUBLIC_KEY = os.environ["RECAPTCHA_PUBLIC_KEY"]
RECAPTCHA_PRIVATE_KEY = os.environ["RECAPTCHA_PRIVATE_KEY"]
