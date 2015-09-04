#!/usr/bin/env bash

# @author Tony Beltramelli
# www.tonybeltramelli.com

# Handle arguments
if [ $# -eq 0 ]
	then
	echo "Error: no arguments supplied"
	echo "Usage:"
	echo "	-m|--mobile <serial mobile device>"
	echo "	-w|--wear <serial wearable device>"
	echo "Run ./adb devices to list serial numbers"
	exit 1
elif [ $# -ne 0 ]
	then
	for i in "$@"
	do
	    PARAM=`echo $1 | awk -F= '{print $1}'`
	    VALUE=`echo $2 | sed 's/^[^=]*=//g'`
	    case $PARAM in
	        -m|--mobile)
				MOBILE_SERIAL=$VALUE
				echo "Mobile serial number $MOBILE_SERIAL"
				;;
	        -w|--wear)
				WEARABLE_SERIAL=$VALUE
				echo "Wearable serial number $WEARABLE_SERIAL"
				;;
	    esac
	    shift
	done
fi

# Build all modules
./gradlew assembleDebug

ROOT=$(cd; pwd)"/Documents/"
ADB_PATH="Android/android-sdk-macosx/platform-tools"

MOBILE_APK="/mobile/build/outputs/apk/mobile-debug.apk"
WEAR_APK="/wear/build/outputs/apk/wear-debug.apk"

SWAT_ROOT=$(cd "$(dirname "$BASH_SOURCE")"; pwd)

# Install apks
cd $ROOT/$ADB_PATH

./adb -s $MOBILE_SERIAL install -r $SWAT_ROOT/$MOBILE_APK
./adb -s $MOBILE_SERIAL shell am start -a android.intent.action.MAIN -n com.tonybeltramelli.swat.mobile/.MainActivity

./adb -s $WEARABLE_SERIAL install -r $SWAT_ROOT/$WEAR_APK
./adb -s $WEARABLE_SERIAL shell am startservice -a com.google.android.gms.wearable.BIND_LISTENER -n com.tonybeltramelli.swat.mobile/.MainService
