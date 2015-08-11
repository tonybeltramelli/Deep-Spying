#!/usr/bin/env bash

# Build all modules
./gradlew assembleDebug

ROOT=$(cd; pwd)"/Documents/"
ADB_PATH="Android/android-sdk-macosx/platform-tools"

MOBILE_APK="/mobile/build/outputs/apk/mobile-debug.apk"
WEAR_APK="/wear/build/outputs/apk/wear-debug.apk"

SWAT_ROOT=$(cd "$(dirname "$BASH_SOURCE")"; pwd)

# Install apks
cd $ROOT/$ADB_PATH

# Run ./adb devices to list serial numbers
./adb -s [serial mobile device] install $SWAT_ROOT/$MOBILE_APK
./adb -s [serial wear device] install $SWAT_ROOT/$WEAR_APK
