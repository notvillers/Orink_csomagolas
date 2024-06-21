const { Client } = require("basic-ftp"); // FTP module

/**
* Class for handling FTP connections
* @param server - the FTP server
* @param user - the FTP user
* @param password - the FTP password
* @param debug - whether to print debug messages
*/
export class ftp {
    
    server: string;
    user: string;
    private password: string;
    debug: boolean;

    constructor(server: string, user: string, password: string, debug: boolean = false) {
        this.server = server;
        this.user = user;
        this.password = password;
        this.debug = debug;
    }

    /**
    * Lists the files in the directory
    * @param directory 
    * @returns the list of files in the directory
    */
    async listFiles(directory: string = "/") {
        const client = new Client();
        client.ftp.verbose = this.debug;
        try {
            await client.access({
                host: this.server,
                user: this.user,
                password: this.password,
                secure: false
            });
            const filesRaw: any = (await client.list(directory))
            client.close();
            let files: string[] = [];
            filesRaw.forEach((file: any) => {
                if (file.type === 1) {
                    files.push(file.name);
                }
            });
            return files;
        } catch(err) {
            console.log(err);
        }
        client.close();
    }

    /**
    * Lists the directories in the directory
    * @param directory 
    * @returns the list of directories in the directory
    */
    async listDirectories(directory: string = "/") {
        const client = new Client();
        client.ftp.verbose = this.debug;
        try {
            await client.access({
                host: this.server,
                user: this.user,
                password: this.password,
                secure: false
            });
            const filesRaw: any = (await client.list(directory))
            client.close();
            let files: string[] = [];
            filesRaw.forEach((file: any) => {
                if (file.type === 2) {
                    files.push(file.name);
                }
            });
            return files;
        } catch(err) {
            console.log(err);
        }
        client.close();
    }

    /**
    * Downloads a file from the FTP server
    * @param remoteFileName
    * @param localFileName
    */
    async downloadFile(remoteFileName: string, localFileName: string) {
        const client = new Client();
        client.ftp.verbose = this.debug;
        try {
            await client.access({
                host: this.server,
                user: this.user,
                password: this.password,
                secure: false
            });
            await client.downloadTo(localFileName, remoteFileName);
            console.log(remoteFileName + " downloaded to " + localFileName);
            
        } catch(err) {
            console.log(err);
        }
        client.close();
    }

    /**
    * Uploads a file to the FTP server
    * @param localFileName
    * @param remoteFileName
    */
    async uploadFile(localFileName: string, remoteFileName: string) {
        const client = new Client();
        client.ftp.verbose = true;
        try {
            await client.access({
                host: this.server,
                user: this.user,
                password: this.password,
                secure: false
            });
            await client.uploadFrom(localFileName, remoteFileName);
        } catch(err) {
            console.log(err);
        }
        client.close();
    }

}