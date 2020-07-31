# Veracode Archer Data Script

Uses the Veracode Archer API to to export data from the Veracode Platform for import into RSA Archer. See the RSA Community for details on configuring RSA Archer to import the resulting output from this file.

## Setup

Clone this repository:

    git clone https://github.com/tjarrettveracode/veracode-archer

Install dependencies:

    cd veracode-archer
    pip install -r requirements.txt

(Optional) Save Veracode API credentials in `~/.veracode/credentials`

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>

## Run

If you have saved credentials as above you can run:

    python vcarcher.py (arguments)

Otherwise you will need to set environment variables before running `vcarcher.py`:

    export VERACODE_API_KEY_ID=<YOUR_API_KEY_ID>
    export VERACODE_API_KEY_SECRET=<YOUR_API_KEY_SECRET>
    python vcarcher.py (arguments)

Arguments supported include:

* **`--interval`, `-i`** : Interval over which to import data. Options: `last-day`, `last-week`, `last-month`, `all-time`, `range` (default: `last-day`).
* **`--from-date`, `-f`** : Optional, required if `range` is specified for `-i`. The date on which to begin the import range (in `mm-dd-yyyy` format).
* **`--to-date, -t`** : Optional, required if `range` is specified for `-i`. The date on which to end the import range (in `mm-dd-yyyy` format).
* **`--scan-type, -s`** : Optional. The scan type to import. Options: `static`, `dynamic`, `manual`.

## Output

The script outputs an XML file that validates to the Veracode [archerreport.xsd schema](https://help.veracode.com/viewer/document/Dq8nUbznNM4qXZ~bC0Zi9A).

## Notes

1. To be able to use the Archer API, you must have an API service account with the Archer Report API role, as described in the [Veracode Help Center](https://help.veracode.com/reader/TNIuE0856bMwmOQldtxbmQ/VCmovHKq7wSDn5AAjxt3nw)
2. Generation of the output file in the Veracode Platform may take some time. The script will run until the file is received.
3. The longer the period (and the more applications included), the longer it takes to generate the Archer Report on the Veracode side. If your report generation takes a very long time, try shortening the period or focusing only on certain scan types.
