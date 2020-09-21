#!/bin/bash

HOSTNAME="localhost"
CONFNAME="rtc_SeqOut_${HOSTNAME}.conf"
COMPNAME="SeqOut.py"

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

manager.components.preactivation: SequenceOutComponent0
manager.components.preconnect: \\
    SequenceOutComponent0.Octet?interface_type=paho_mqtt&host=${HOSTNAME}&topic=octet, \\
    SequenceOutComponent0.Short?interface_type=paho_mqtt&host=${HOSTNAME}&topic=short, \\
    SequenceOutComponent0.Long?interface_type=paho_mqtt&host=${HOSTNAME}&topic=long, \\
    SequenceOutComponent0.Float?interface_type=paho_mqtt&host=${HOSTNAME}&topic=float, \\
    SequenceOutComponent0.Double?interface_type=paho_mqtt&host=${HOSTNAME}&topic=double, \\
    SequenceOutComponent0.OctetSeq?interface_type=paho_mqtt&host=${HOSTNAME}&topic=octetseq, \\
    SequenceOutComponent0.ShortSeq?interface_type=paho_mqtt&host=${HOSTNAME}&topic=shortseq, \\
    SequenceOutComponent0.LongSeq?interface_type=paho_mqtt&host=${HOSTNAME}&topic=longseq, \\
    SequenceOutComponent0.FloatSeq?interface_type=paho_mqtt&host=${HOSTNAME}&topic=floatseq, \\
    SequenceOutComponent0.DoubleSeq?interface_type=paho_mqtt&host=${HOSTNAME}&topic=doubleseq
EOF

#############
# Launch RTC
${python_cmd} ${comp_path} -f ${CONFNAME}



