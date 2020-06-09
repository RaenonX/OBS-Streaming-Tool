# OBS Streaming Tool

This was created to enable marquee (with pause) effect in OBS and to share the rendering work with OBS.

## Known advantages

- Have a marquee effect that OBS does not have.

- Sharing the rendering work with OBS to reduce rendering lag.

- Low system resource usage while highly customizable.

## Notes

- Developed under Python 3.8.

- Running from multiple sources may result in some contents being skipped.

- Add Custom CSS in `Browser Source` with selector `body` to configure some global style, for example, `font-size`.

## Usage

1. Run `py -m flask run`.

    - Be sure to install `flask` in your Python environment.

2. Create a `Browser Source` in OBS with the URL which flask is running on. Default to `http://127.0.0.1/5000`.

    - The height is defaulted to `100vh`. The height of the window.
    
    - All things above are customizable by modifying `templates/main.html`.
    
For more functions, check the [endpoints](#endpoints) section.

## Setup

### Marquee

There are 3 components of the marquee:

- `[FILE]` [Foobar2K Now Playing](#Foobar2K-Now-Playing)

- `[FILE]` [Static Text](#Static-Text)

- `[API]` [Youtube Data API (v3)](#Youtube-Data-API)

    - Currently only support "current viewers"

> To "install" or "uninstall" the component, go to `content.py` and change the variable `input_fns`.

`FILE` Components

- There's a `Path` field in `config.ini` to specify the file path for the corresponding component.

- The first line of the file needs to be `1`, or the rest of the file will not be read.

#### `Foobar2K Now Playing`

- Setup

    - Install `foo_np_simple`.
    
    - Setup the output using `$crlf()` to separate lines(outputs) in FB2K. 
    
        - Remember that the first line will indicate if the file will be read. Anything besides `1` will skip the read.
        
    - Copy the file output path, and paste it under `Foobar2K/Path` in `config.ini`.
    
#### `Static Text`

- Setup

    - Create a text file somewhere.
    
    - Insert the text you want to display. Use newline to separate them.
    
        - Remember that the first line will indicate if the file will be read. Anything besides `1` will skip the read.

    - Remember the file path, and set it under `StaticText/Path` in `config.ini`.
    
- Note

    - An empty line **with** a white space will be considered as the content separator in the static texts.
    
        - Output flow: `FB2K -> Static Text -> Youtube -> FB2K -> ...`

    - An empty line **without** a white space will make the static texts being outputted separately.
    
        - Output flow: `FB2K -> Static Text (Section 1) -> Youtube -> FB2K -> Static Text (Section 2) -> Youtube -> FB2K -> Static Text (Section 1)...`
        
    - Lines beginning with `//` will be skipped.
    
#### `Youtube Data API`
   
- Setup
   
    - Environment variable `YT_VIDEO_ID`: The video ID to track the current viewers
    
    - Environment variable `YT_API_KEY`: The API key acquired using Google Cloud Console
    
- Note

    - Output will be skipped if the current viewer is 0 or inaccessible.
    
### Current datetime `[CurrentDatetime]`

There are a few items to be configured in `config.ini`:

- `Timezone`: list of timezones to be displayed. Separated by comma `,`.

    - Must be the `pytz` timezone identifiers. 
    
    - List of the available identifiers can be found [here](https://stackoverflow.com/q/13866926/11571888)
    
    - Some common identifiers: `Asia/Taipei` `US/Pacific` `US/Mountain` `US/Central` `US/Eastern`
    
- `ToNext`: Count of the calls to change to the timezone.

### Timer

There is a configurable setting in `config.ini`:

- `DisplaySec`: Time length in second(s) from time up to display the timer and remove the end message 
                if `up` is `1` and `end_msg` is given. 

## Endpoints

### To be used on OBS


#### `/`

Marquee with styles applied.

/ Stylable CSS selector | Description |
| :---: | :---: |
| `div#content` | Content of the marquee |

#### `/dt`

Current timestamp expression with styles applied.

Automatically update once a second. 
This can be changed by modifying [`the js in the corresponding template`](/templates/current_dt.html#L33).

The timezone for the current time will constantly switching between the configured timezone. 
Check [this section](#Current-datetime) for configuring the corresponding settings.

/ Stylable CSS selector | Description |
| :---: | :---: |
| `span#date` | Date expression |
| `span#time` | Time expression |
| `span#tz` | Timezone expression |

#### `/timer`

Current timer status with styles applied.

Automatically update once a second. 
This can be changed by modifying [`the js in the corresponding template`](/templates/current_dt.html#L36).

| Parameter | Description | Type | Valid Values |
| :---: |  :-------: |  :---: |  :---: | 
| `dt` | Target datetime of the timer. | Required | Any expression that could be understood by `python-dateutil`'s parser. |
| `up` | If the timer should count up. | Optional | `0` or `1` |
| `end_msg` | End message of the timer. | Optional | Any string |

| Stylable CSS selector | Description |
| :---: | :---: |
| `div.count-up` | Timer which is counting up (now > dt) |
| `div.count-down` | Timer which is counting down (dt > now) |
| `div.message` | Timer which is expired, displaying end message |


#### `/chrono`

Similar to [/timer](#timer). The only difference is that [/timer](#timer) uses a timestamp as the changing point, 
while this receives a time offset. The time offset will be counted down first, then do the same behavior as [/timer](#timer).

The chrono will restart if the `Browser Source` is refreshed.

To start counting up at the beginning, set the time with a negative value.

For example, to start counting up from 34 mins, set the parameter as `...?m=-34`.

| Parameter | Description | Type | Valid Values |
| :---: |  :-------: |  :---: |  :---: | 
| `d` | Days of the time offset. | Optional | Any numeric value |
| `h` | Hours of the time offset. | Optional | Any numeric value |
| `m` | Minutes of the time offset. | Optional | Any numeric value |
| `s` | Seconds of the time offset. | Optional | Any numeric value |
| `up` | If the timer should count up. | Optional | `0` or `1` |
| `end_msg` | End message of the timer. | Optional | Any string |

| Stylable CSS selector | Description |
| :---: | :---: |
| `div.count-up` | Timer which is counting up (now > dt) |
| `div.count-down` | Timer which is counting down (dt > now) |
| `div.message` | Timer which is expired, displaying end message |

### For internal use or deeper customization


#### `/content/marquee`

Pure text of the next content of the marquee.


#### `/content/dt`

Pure text of the current time.


#### `/content/timer`

Current timer status with styles applied.

| Parameter | Description | Type | Valid Values |
| :---: |  :-------: |  :---: |  :---: | 
| `dt` | Target datetime of the timer. | Required | Any expression that could be understood by `python-dateutil`'s parser. |
| `up` | If the timer should count up. | Optional | `0` or `1` |
| `end_msg` | End message of the timer. | Optional | Any string |