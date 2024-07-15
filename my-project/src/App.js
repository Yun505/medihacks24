import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useReactMediaRecorder } from "react-media-recorder";
import medi from './Logo.png';
import './App.css';

const RecordView = () => {
  const [second, setSecond] = useState("00");
  const [minute, setMinute] = useState("00");
  const [isActive, setIsActive] = useState(false);
  const [counter, setCounter] = useState(0);
  const [downloadUrl, setDownloadUrl] = useState(null);
  const [userInput, setUserInput] = useState("");
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    let intervalId;

    if (isActive) {
      intervalId = setInterval(() => {
        const secondCounter = counter % 60;
        const minuteCounter = Math.floor(counter / 60);

        let computedSecond =
          String(secondCounter).length === 1
            ? `0${secondCounter}`
            : secondCounter;
        let computedMinute =
          String(minuteCounter).length === 1
            ? `0${minuteCounter}`
            : minuteCounter;

        setSecond(computedSecond);
        setMinute(computedMinute);

        setCounter((counter) => counter + 1);
      }, 1000);
    }

    return () => clearInterval(intervalId);
  }, [isActive, counter]);

  function stopTimer() {
    setIsActive(false);
    setCounter(0);
    setSecond("00");
    setMinute("00");
  }

  const {
    status,
    startRecording,
    stopRecording,
    pauseRecording,
    mediaBlobUrl
  } = useReactMediaRecorder({
    video: false,
    audio: true,
    echoCancellation: true
  });

  useEffect(() => {
    if (mediaBlobUrl) {
      setDownloadUrl(mediaBlobUrl);
    }
  }, [mediaBlobUrl]);

  const handleStopRecording = () => {
    stopRecording();
    pauseRecording();
    stopTimer();
  };

  const handleInputChange = (event) => {
    setUserInput(event.target.value);
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/talk', {
        user_input: userInput,
      });
      setMessages([...messages, { sender: 'user', text: userInput }, { sender: 'bot', text: response.data.messages }]);
      setUserInput("");  // Clear input after submission
    } catch (error) {
      console.error("Error sending the message:", error);
    }
  };

  return (
    <div>
      <div
        style={{
          border: "1px solid black",
          backgroundColor: "black",
          width: "100%",
          height: "350px",
          padding: "10px",
          boxSizing: "border-box"
        }}
      >
        <div style={{ backgroundColor: "black", color: "white", textAlign: "center", marginTop: "10px" }}>
          <button
            style={{
              backgroundColor: "black",
              borderRadius: "8px",
              color: "white",
              padding: "5px 10px",
              marginBottom: "10px"
            }}
            onClick={stopTimer}
          >
            Clear
          </button>
          <div style={{ fontSize: "54px" }}>
            <span className="minute">{minute}</span>
            <span>:</span>
            <span className="second">{second}</span>
          </div>

          <div style={{ marginTop: "20px", display: "flex", justifyContent: "center" }}>
            <button
              style={{
                padding: "0.8rem 2rem",
                border: "none",
                margin: "0 15px",
                fontSize: "1rem",
                cursor: "pointer",
                borderRadius: "5px",
                fontWeight: "bold",
                backgroundColor: isActive ? "#df3636" : "#42b72a",
                color: "white",
                transition: "all 300ms ease-in-out",
                transform: "translateY(0)"
              }}
              onClick={() => {
                if (!isActive) {
                  startRecording();
                } else {
                  pauseRecording();
                }
                setIsActive(!isActive);
              }}
            >
              {isActive ? "Pause" : "Start"}
            </button>
            <button
              style={{
                padding: "0.8rem 2rem",
                border: "none",
                backgroundColor: "#df3636",
                marginLeft: "15px",
                fontSize: "1rem",
                cursor: "pointer",
                color: "white",
                borderRadius: "5px",
                fontWeight: "bold",
                transition: "all 300ms ease-in-out",
                transform: "translateY(0)"
              }}
              onClick={handleStopRecording}
            >
              Stop
            </button>
          </div>

          {downloadUrl && (
            <a
              href={downloadUrl}
              download={`recording_${minute}_${second}.mp3`}
              style={{
                padding: "0.8rem 2rem",
                border: "none",
                backgroundColor: "#4CAF50",
                color: "white",
                borderRadius: "5px",
                fontWeight: "bold",
                textDecoration: "none",
                display: "inline-block",
                marginTop: "15px"
              }}
            >
              Download Recording
            </a>
          )}
        </div>
      </div>

      <form onSubmit={handleFormSubmit} style={{ marginTop: "20px", textAlign: "center", display: 'flex', justifyContent: 'center' }}>
        <input
          type="text"
          value={userInput}
          onChange={handleInputChange}
          placeholder="Type your message"
          style={{
            padding: "10px",
            borderRadius: "5px 0 0 5px",
            border: "1px solid #ccc",
            width: "300px"
          }}
        />
        <button
          type="submit"
          style={{
            padding: "10px 20px",
            borderRadius: "0 5px 5px 0",
            border: "none",
            backgroundColor: "#42b72a",
            color: "white",
            cursor: "pointer"
          }}
        >
          Send
        </button>
      </form>

      <div style={{ marginTop: "20px", textAlign: "center" }}>
        {messages.map((message, index) => (
          <p key={index} style={{ color: message.sender === 'user' ? 'blue' : 'green' }}>
            {message.text}
          </p>
        ))}
      </div>
    </div>
  );
};

function App() {
  return (
    <div>
      <div className="navbar bg-gradient-to-r from-error to-warning text-primary-content">
        <a className="btn btn-ghost text-xl">Documentation</a>
      </div>
      <div className="hero bg-base-200 min-h-screen">
        <div className="hero-content flex-col lg:flex-row-reverse">
          <img
            src={medi}
            className="max-w-sm rounded-lg shadow-2xl"
            alt="Logo"
          />
          <div>
            <br />
            <h1 className="text-5xl font-bold text-error">Emergency Dispatch Detection</h1>
            <br className="py-9" />
            <h1 className="text-2xl text-base-400 font-bold">Meet Your Lifesaving Chatbot!</h1>
            <br className="py-3" />
            <p>
              Introducing our <b>cutting-edge chatbot</b>, designed with a powerful Retrieval-Augmented Generation (RAG) layer. This isn't just any chatbot – it's your <u>personal crisis responder</u>, ready to jump into action at a moment's notice.
            </p>
            <p>
              Need someone to talk to? Our chatbot <b>connects</b> you with the right people for support. Facing an emergency? It assesses the urgency and calls <b>911</b> for you! Plus, it guides you through essential steps to ensure you handle any situation like a pro.
            </p>
            <p>
              With our chatbot, you're <b>never alone.</b> Feel the confidence of knowing help is just a message away. Get ready to experience the future of crisis management!
            </p>
            <br className="py-5" />
            <button className="btn btn-primary" onClick={() => document.getElementById('my_modal_5').showModal()}>
              Chat With Us!
            </button>
            <dialog id="my_modal_5" className="modal modal-bottom sm:modal-middle">
              <div className="modal-box">
                <h3 className="font-bold text-lg">Please Record your problem</h3>
                <p className="py-4">Click Submit for our model to diagnose your problem, an alert will show up if we have called 911 on your behalf</p>
                <div className="modal-action">
                  <RecordView />
                  <form method="dialog">
                    <button className="btn btn-xs sm:btn-sm md:btn-md lg:btn-lg">Close</button>
                  </form>
                </div>
              </div>
            </dialog>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
