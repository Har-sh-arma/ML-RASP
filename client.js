let flag = true;
let pc = null;

var dc = null, dcInterval = null;
let accelerometer = null;
let message = ""
let selected_cam = null;
let currentStream;
let d = new Date();
let curr_time = d.getTime();

const negotiate = () => {
    return pc.createOffer().then((o) => {
        console.log(`Created Offer : ${o}`);
        pc.setLocalDescription(o);
    }, (err) => {
        console.error(`Error [Set Local Desc]:${err}`);
    }).then(() => {
        return new Promise((resolve, reject) => {
            if (pc.iceGatheringState === 'complete') {
                resolve("Ice Gathering Complete")
            }
            else {
                checkState = () => {
                    if (pc.iceGatheringState === 'complete') {
                        pc.removeEventListener('icegatheringstatechange', checkState)
                        resolve('Ice Gathering Complete !!!')
                    }
                    else {
                        console.log("Gathering Candidates ...");
                    }
                }
                pc.addEventListener('icegatheringstatechange', checkState)
            }
        })
    }).then(() => {
        let offer = pc.localDescription;
        return axios.post('/offer', { sdp: offer.sdp, type: offer.type, video_transform: 'none' })
    }).then((res) => {
        pc.setRemoteDescription(res.data)
        console.log(pc.remoteDescription);
    })
}

const start = () => {
    pc = new RTCPeerConnection();
    
    if (typeof currentStream !== 'undefined') {
        stopMediaTracks(currentStream);
      }

    navigator.mediaDevices.getUserMedia({ video: {deviceId:selected_cam}, audio: false}).then(
        (stream) => {
            stream.getTracks().forEach(
                (track) => {
                    pc.addTrack(track, stream);
                }
            );
            return negotiate();
        }, (err) => {
            console.error(`Error getting UserMedia: ${err}`)
        }
    )
}


function stopMediaTracks(stream) {
    stream.getTracks().forEach(track => {
      track.stop();
    });
  }
  


let video = document.getElementsByTagName("video")[0]
let camopt = document.getElementById("camoptions")
navigator.mediaDevices.enumerateDevices().then((mediaDevices)=>{
    mediaDevices.forEach((mediaDevice)=>{
        if(mediaDevice.kind === "videoinput"){
            let but = document.createElement("button");
            but.innerText = mediaDevice.deviceId;
            but.onclick = (event)=>{
                if (typeof currentStream !== 'undefined') {
                    stopMediaTracks(currentStream);
                  }
                selected_cam = event.target.innerText;
                console.log(selected_cam);
                navigator.mediaDevices.getUserMedia({ video: {"deviceId":selected_cam}, audio:false}).then(
                    (stream) =>{
                        currentStream = stream
                        video.srcObject = stream
                        console.log("Src object set");
                  }).catch((err)=>{console.log(err);})
            }
            camopt.appendChild(but)
        }
    })
});


