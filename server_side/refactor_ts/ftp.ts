import { log } from "console";

const { Client } = require("basic-ftp");

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
            var files: string[] = [];
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
            var files: string[] = [];
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
        } catch(err) {
            console.log(err);
        }
        client.close();
    }

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