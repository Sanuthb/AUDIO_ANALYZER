import express from "express";
import mongoose from "mongoose";
import cors from "cors";
import path from "path";
import audiorecord from "./Routes/audiorecorder.js";
import audioanalyze from "./Routes/audioanalyzer.js";
import {__dirname } from "./uttils.js"

const app = express();
app.use(cors());
app.use(express.json());
app.use(
  "/uploaded_files",
  express.static(path.join(__dirname, "pythonoutput"))
);
app.use("/audiorecord",audiorecord)
app.use("/audioanalyze", audioanalyze);

mongoose
  .connect(
    `mongodb+srv://sanuthbibin:pFtzxOlOxASzi9ds@cluster0.txp0xqk.mongodb.net/bookstore?retryWrites=true&w=majority&appName=Cluster0`
  )
  .then(() => {
    console.log("mongodb running..");
    app.listen(8000, () => {
      console.log("Server is running on port 8000");
    });
  })
  .catch((err) => {
    console.log(err);
  });
