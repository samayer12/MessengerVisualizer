#!/usr/bin/env bash
if [[ $(find ../output/ | wc -l) -gt 1 ]]; then
  rm -r ../output/*
fi
