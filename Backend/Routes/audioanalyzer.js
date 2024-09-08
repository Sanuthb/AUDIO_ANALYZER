import express from "express";
import { exec } from "child_process";
import path from "path";
import { fileURLToPath } from "url";
import { dirname } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const audioanalyze = express.Router();

const scriptPath = path.join(__dirname, "../pythonfiles/analyze_audio.py");
const audioFile = path.join(__dirname, "../pythonoutput/output.wav");

audioanalyze.get("/", (req, res) => {
  exec(`python "${scriptPath}" "${audioFile}"`, (error, stdout, stderr) => {
    if (error) {
      console.error(`error: ${error.message}`);
      return res.status(500).send("Server Error");
    }
    if (stderr) {
      console.error(`stderr: ${stderr}`);
      return res.status(500).send("Server Error");
    }
    try {
      const result = JSON.parse(stdout);
      res.json(result);
    } catch (parseError) {
      console.error(`parseError: ${parseError.message}`);
      res.status(500).send("Error parsing Python script output");
    }
  });
});

export default audioanalyze;
