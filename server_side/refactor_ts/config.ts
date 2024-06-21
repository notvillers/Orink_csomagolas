const path = require('path');
const fs = require('fs');

export const pathDirectory: string = __dirname;

export const remoteDirectory: string = "csomagolas";

const localDirectory: string = "logs";
export const localPath: string = path.join(pathDirectory, localDirectory);
if (!fs.existsSync(localPath)) {
    fs.mkdirSync(localPath);
}