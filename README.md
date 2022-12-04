![Logo](https://github.com/maantjemol/EoCS-project/blob/master/logo.png?raw=true)

A web email service in python without the use of external libraries.

## Installation

Clone the project to your system with

```bash
git clone https://github.com/maantjemol/EoCS-project.git
```

Install the included ssl certificates `rootCA.pem` in the `cert` folder to your system. There are guides available for [Windows](https://windowsreport.com/install-windows-10-root-certificates/) and [Mac (only follow step 2)](https://www.freecodecamp.org/news/how-to-get-https-working-on-your-local-development-environment-in-5-minutes-7af615770eec/#step-2-trust-the-root-ssl-certificate).

## Usage/Examples

View the finished product at [e-meeuw.de](https://e-meeuw.de)

Or start the server on [https://localhost:1115](https://localhost:1115) with:

```bash
python3 mailserver.py
```

## Documentation

- [Web Server](https://github.com/maantjemol/EoCS-project/blob/master/documentation/webserver.md)
- [Email Server](https://github.com/maantjemol/EoCS-project/blob/master/documentation/emailserver.md)
## License

[MIT](https://choosealicense.com/licenses/mit/)
