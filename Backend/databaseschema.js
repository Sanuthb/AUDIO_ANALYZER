import mongoose from "mongoose";

const audioSchema = new mongoose.Schema({
  filename: String,
  contentType: String,
  fileData: Buffer,
  metadata: {
    userId: String,
    description: String,
  },
  uploadDate: { type: Date, default: Date.now },
});

export const AudioFile = mongoose.model("AudioFile", audioSchema);

