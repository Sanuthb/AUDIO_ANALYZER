import React, { useState } from "react";
import axios from "axios";
import './App.css'

const App = () => {
  const [status, setStatus] = useState("Press button to record...");
  const [audioUrl, setAudioUrl] = useState("");
  const [analysedData, setAnalysedData] = useState({});

  const handleRecordAudio = async () => {
    try {
      setStatus("Recording audio...");
      const response = await axios.get("http://localhost:8000/audiorecord");
      const file = response.data;

      if (file) {
        const fileUrl = `http://localhost:8000/uploaded_files/${file}`;
        setAudioUrl(fileUrl);
        setStatus("Recording successful. Playing audio...");
      } else {
        setStatus("Failed to record audio.");
      }
    } catch (error) {
      console.error(error);
      setStatus("An error occurred while recording.");
    }
  };

  const handleAudioAnalyze = async () => {
    try {
      const response = await axios.get("http://localhost:8000/audioanalyze");
      const data = response.data;

      if (data) {
        setAnalysedData(data);
      } else {
        setAnalysedData({}); 
      }
    } catch (error) {
      console.error(error);
      setAnalysedData({ error: "An error occurred during analysis." });
    }
  };

  return (
    <div className="app">
      <button onClick={handleRecordAudio} className="btn">Record Audio</button>
      <p className="status">{status}</p>
      {audioUrl && (
        <div className="audio_data">
          <audio controls>
            <source src={audioUrl} type="audio/wav" />
            Your browser does not support the audio element.
          </audio>
          <button className="btn" onClick={handleAudioAnalyze}>Analyze Audio</button>
          <div className="extracteddata">
            {analysedData.error ? (
              <p>{analysedData.error}</p>
            ) : (
              <pre>{JSON.stringify(analysedData, null, 2)}</pre> 
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
