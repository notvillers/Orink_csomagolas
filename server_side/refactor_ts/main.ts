const fs = require('fs');
const path = require('path');
import { pathDirectory, remoteDirectory, localPath } from './config';
import { ftp } from './ftp';

(async () => {
    const ftpJson = JSON.parse(fs.readFileSync("./ftp.json", "utf8"));
    const ftpClient: ftp = new ftp(ftpJson.hostname, ftpJson.username, ftpJson.password, true);
    const file_names: any = await ftpClient.listFiles(remoteDirectory);
    for (let file_name of file_names) {
        ftpClient.downloadFile(path.join(remoteDirectory, file_name), path.join(localPath, file_name));
    }
})();