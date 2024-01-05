import React, { Fragment, useEffect } from "react";
import axios from "axios";
import { LoadingOutlined } from '@ant-design/icons';

var userEmail = "my mail"
var registrantToken = ''
var zakToken = ''
var leaveUrl = `http://localhost:3000`
const antIcon = <LoadingOutlined />;

const MeetingComponent= () => {
    const userName = "YourUserName"; 
    useEffect( () => {
        getSignature();
    }, []);
    const getSignature = async () => {
        await axios({
            method: 'get',
            url: `http://localhost:8000/api/meeting/authorize`,
            data: { meeting_no: '88912157619', role: 0 }, // 0 = participant, 1 = host.
            headers: {
                Authorization: "NNtB66DNQsWxRPzwm2EhPA"
            }
        }).then(res => {
            const data = res.data.data;
            initMeeting(data);
        }).catch((err) => {
            console.log(err)
        })
    }
    const initMeeting = async (data) => {
        const { ZoomMtg } = await import('@zoomus/websdk');
        ZoomMtg.setZoomJSLib('https://source.zoom.us/2.18.2/lib', '/av');
        ZoomMtg.preLoadWasm();
        ZoomMtg.prepareWebSDK();
    
        ZoomMtg.i18n.load('en-US');
        ZoomMtg.i18n.reload('en-US');
        ZoomMtg.init({
            leaveUrl: leaveUrl,
            success: (success) => {
                ZoomMtg.join({
                    signature: data.token,
                    sdkKey: data.sdkKey,
                    meetingNumber: data.meeting_no,
                    passWord: data.password,
                    userName: userName,
                    userEmail: userEmail,
                    tk: registrantToken,
                    zak: zakToken,
                    success: (success) => {
                        console.log(success)
                    },
                    error: (error) => {
                        console.log(error)
                    }
                })
            },
            error: (error) => {
                console.log(error)
            }
        })
    }
    return (<Fragment> </Fragment>
    );
}
export default MeetingComponent;