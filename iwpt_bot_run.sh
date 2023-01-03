#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
readonly SCRIPT_DIR

date
# shellcheck source=/dev/null
. "$"{SCRIPT_DIR}/venv"
python "${SCRIPT_DIR}/iwpt_bot.py"
