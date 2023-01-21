#!/usr/bin/env python3

import os
import unflipper

log_level = os.environ.get("UNFLIPPER_LOG_LEVEL", "INFO").upper()

client = unflipper.Unflipper(log_level=log_level)
client.run(os.environ.get('UNFLIPPER_TOKEN'))