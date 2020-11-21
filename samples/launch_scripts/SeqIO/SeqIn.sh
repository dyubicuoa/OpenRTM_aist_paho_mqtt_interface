#!/bin/bash

HOSTNAME="localhost"
CONFNAME="rtc_SeqIn_${HOSTNAME}.conf"
COMPNAME="SeqIn.py"

comp2_path=`dpkg -L openrtm-aist-python-example |grep ${COMPNAME}`
comp3_path=`dpkg -L openrtm-aist-python3-example |grep ${COMPNAME}`

############################################
# Check RTC's path
# RTC's path is set to "comp_path"
if test "x" = "x$comp3_path" ; then
    if test "x" = "x$comp2_path" ; then
	echo "${COMPNAME} not found. Aborting."
	exit 1
    else
	comp_path=${comp2_path}
	python_cmd="python2"
    fi
else
    comp_path=${comp3_path}
    python_cmd="python3"
fi

############################################
# Check Paho MQTT module
# Paho MQTT module path is set to "mod_path" 
if test "xpython3" = "x${python_cmd}" ; then
    mod3_path=`pip3 show OpenRTM_aist_paho_mqtt_module | grep Location | awk '{print $2;}'`
    if test "x" = "x${mod3_path}" ; then
	echo "Paho MQTT module for OpenRTM-aist not found. Aborting."
	exit 1
    fi
    mod_path=${mod3_path}/OpenRTM_aist_paho_mqtt_module
elif test "xpython2" = "x${python_cmd}" ; then
    mod2_path=`pip2 show OpenRTM_aist_paho_mqtt_module | grep Location | awk '{print $2;}'`
    if test "x" = "x${mod2_path}" ; then
	echo "Paho MQTT module for OpenRTM-aist not found. Aborting."
	exit 1
    fi
    mod_path=${mod2_path}/OpenRTM_aist_paho_mqtt_module
else
    echo "Unknown error. (never comes here)"
    exit 1
fi
echo "python:    " ${python_cmd}
echo "comp_path: " ${comp_path}
echo "mod_path:  " ${mod_path}

######################
# Generating rtc.conf
cat << EOF > ${CONFNAME}
logger.enable: YES
logger.log_level: DEBUG

manager.modules.load_path: ${mod_path}
manager.modules.preload: InPortPahoSubscriber.py, OutPortPahoPublisher.py

manager.components.preactivation: SequenceInComponent0
manager.components.preconnect: \\
    SequenceInComponent0.Octet?interface_type=mqtt_cdr&host=${HOSTNAME}&topic=octet, \\
    SequenceInComponent0.Short?interface_type=mqtt_cdr&host=${HOSTNAME}&topic=short, \\
    SequenceInComponent0.Long?interface_type=mqtt_cdr&host=${HOSTNAME}&topic=long, \\
    SequenceInComponent0.Float?interface_type=mqtt_cdr&host=${HOSTNAME}&topic=float, \\
    SequenceInComponent0.Double?interface_type=mqtt_cdr&host=${HOSTNAME}&topic=double, \\
    SequenceInComponent0.OctetSeq?interface_type=mqtt_cdr&host=${HOSTNAME}&topic=octetseq, \\
    SequenceInComponent0.ShortSeq?interface_type=mqtt_cdr&host=${HOSTNAME}&topic=shortseq, \\
    SequenceInComponent0.LongSeq?interface_type=mqtt_cdr&host=${HOSTNAME}&topic=longseq, \\
    SequenceInComponent0.FloatSeq?interface_type=mqtt_cdr&host=${HOSTNAME}&topic=floatseq, \\
    SequenceInComponent0.DoubleSeq?interface_type=mqtt_cdr&host=${HOSTNAME}&topic=doubleseq
EOF

#############
# Launch RTC
${python_cmd} ${comp_path} -f ${CONFNAME}


