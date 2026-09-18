#! /bin/bash

pixi run --script inspect_bundle.py test.bundle.json | jq .
