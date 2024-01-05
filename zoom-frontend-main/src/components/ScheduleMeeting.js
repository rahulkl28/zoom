import React, { useState } from 'react';
import axios from "axios";


function ScheduleMeeting() {
  const [topic, setTopic] = useState(null);
  const [agenda, setAgenda] = useState(null);
  const [startTime, setStartTime] = useState(null);

  const scheduleAPI = async () => {
    await axios({
      method: 'get',
      url: `http://localhost:8000/api/meeting/create`,
      data: { topic: topic, agenda: agenda, start_time: startTime }, // YYYY-MM-DD hh:mm
      headers: {
        Authorization: "NNtB66DNQsWxRPzwm2EhPA"
      }
    }).then(res => {
      console.log("Meeting successfully created!")
    }).catch((err) => {
      console.log(err)
    })
  }
  return (
    <div style={{ textAlign: "center" }}>
      <input onChange={(e) => setTopic(e.target.value)} placeholder='enter topic'></input> <br /><br />
      <input onChange={(e) => setAgenda(e.target.value)} placeholder='enter agenda'></input><br /><br />
      <input onChange={(e) => setStartTime(e.target.value)} placeholder='enter start datetime'></input><br />
      <small>format: YYYY-MM-DD HH:mm</small>
      <br /><br />
      <button onClick={scheduleAPI}>Schedule</button>
    </div>
  );
}
export default ScheduleMeeting;