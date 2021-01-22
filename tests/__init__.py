import os

# Make sure that tests do not use the same redis database
# TODO this is not great and should probably be improved
os.environ["OXCT_REDIS_DB"] = "1"
