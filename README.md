# ProjectorController

ProjectorController is a CLI written in Python which eases communication with Christie Digital® projectors supporting TCP/IP serial commands.

## Installation

### Prerequisites

- Python 3

### Clone

- Clone this repo to your local machine using `https://github.com/alexbrt/ProjectorController`

### Setup

ProjectorController was coded to support email status reporting. Unless a valid `./src/smtp_credentials.txt` file is created, the software will most likely crash - this should be fixed in a future version.

> ./src/smtp_credentials.txt syntax

```
user = <email>
password = <password>
recipients = <email_1>, <email_2>, ...
```
**Note:** Until this gets fixed, if you want to run the program without email status reporting, you can simply delete the code from `./src/main.py` which parses the `.txt` file. However, executing the `update_loop_email` command will still result in a crash.

## Usage

**Note:** This software can currently only be used as a standalone tool - API is coming soon.

- For Windows users, execute `./windows/run.bat`

- For Unix users, execute `./unix/run.sh`

Afterwards, just follow the on-screen instructions. For help, type `-h` or `--help` on the command line.

## Contributing

Pull requests are welcome. For major changes or feature requests, please open an issue first to discuss your needs.

## License

This project is licensed under the terms of the [GNU General Public License Version 3](https://www.gnu.org/licenses/gpl-3.0.en.html) for non-commercial use only.
