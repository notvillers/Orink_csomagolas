const fs = require('fs'); // File system module
const path = require('path'); // Path module
import { debug, pathDirectory, remoteDirectory, localPath } from './config'; // Importing configs
import { ftp } from './ftp'; // Importing the FTP class

// Main function
(async () => {
    // Reading the json for the FTP connection
    const ftpJson = JSON.parse(fs.readFileSync("./ftp.json", "utf8"));

    // Creating the FTP client
    const ftpClient: ftp = new ftp(ftpJson.hostname, ftpJson.username, ftpJson.password, debug);

    // Getting the file names from the remote directory
    const fileNames: any = await ftpClient.listFiles(remoteDirectory);

    // Downloading the files
    for (let fileName of fileNames) {
        ftpClient.downloadFile(path.join(remoteDirectory, fileName), path.join(localPath, fileName));
    }
})();