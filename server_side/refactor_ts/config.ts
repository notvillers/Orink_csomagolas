const fs = require('fs'); // File system module
const path = require('path'); // Path module

// Debug
export const debug: boolean = true;

// The directory of the script
export const pathDirectory: string = __dirname;

// The remote directory
export const remoteDirectory: string = "csomagolas";

// The local directory
const localDirectory: string = "logs";
export const localPath: string = path.join(pathDirectory, localDirectory);
// Create the local directory if it doesn't exist
if (!fs.existsSync(localPath)) {
    fs.mkdirSync(localPath);
}

// The FTP file
const ftpFile: string = "ftp.json";
export const ftpPath: string = path.join(pathDirectory, ftpFile);

// The login file
const loginFile: string = "login.json";
export const loginPath: string = path.join(pathDirectory, loginFile);