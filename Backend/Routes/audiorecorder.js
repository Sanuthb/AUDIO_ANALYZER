import express from 'express'
import path from 'path'
import {exec} from 'child_process'
import { error } from 'console'
import { stderr, stdout } from 'process'

const audiorecord = express.Router()

const scriptpath = path.join('pythonfiles', 'record_audio.py')


audiorecord.get('/', (req, res) => {
    exec(`python ${scriptpath}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`error: ${error.message}`);
            return res.status(500).send('Server Error');
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return res.status(500).send('Server Error');
        }
        const outputFile = stdout.trim(); 

        res.json(outputFile);
    })
})


export default audiorecord