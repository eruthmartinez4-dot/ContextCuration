# Side Project: Balcony Garden Soil Sensor

Started: 2026-06-14
Last updated: 2026-07-20

## What it does

A small microcontroller reads soil moisture in my balcony planters and sends a notification when a planter is too dry.

## Hardware

- ESP32-C3 development board.
- Two capacitive soil moisture sensors (v1.2), one per planter.
- Powered by USB from an outlet on the balcony.

## Software

- Firmware is written in Rust using the esp-hal crate. I chose Rust as a learning exercise.
- Readings are published every 15 minutes over MQTT to Home Assistant running on a Raspberry Pi 4.
- Home Assistant sends a phone notification when moisture drops below 32 percent for two consecutive readings.

## Plants

- Planter A: two 'Sungold' cherry tomato plants.
- Planter B: Genovese basil and flat-leaf parsley.

## Calibration notes

- Dry air reading: 3,180 raw. Fully submerged in water: 1,420 raw.
- Moisture percent is a linear map between those two values, clamped to 0 to 100.
- The 32 percent threshold came from watching when the tomato leaves started to droop.

## Known issues

- Rust compile times on the laptop are slow and the toolchain setup took a full weekend.
- The sensor in planter B reads about 5 points high after rain.
