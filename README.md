# OBS Streaming Tool

This was created to enable marquee (with pause) effect in OBS and to share the rendering work with OBS.

### Known personal advantage

- Have a marquee effect that OBS does not have.

- Sharing the rendering work with OBS to reduce rendering lag.

### Notes

- Developed under Python 3.8.

- Running from multiple sources will result in some contents being skipped.

### Usage

1. Run `py -m flask run`.

    - Be sure to install `flask` in your Python environment.

2. Create a `Browser Source` in OBS with the URL which flask is running on. Default to `http://127.0.0.1/5000`.

    - The height is defaulted to `100vh`. The height of the window.
    
    - All things above are customizable by modifying `templates/main.html`.
    
For more functions, check the [endpoints](#endpoints) section.

### Setup

There are 3 components of this tool:

- `[FILE]` Foobar2K Now Playing

- `[FILE]` Static Text

- `[API]` Youtube Data API (v3)

    - Currently only support "current viewers"

> To "install" or "uninstall" the component, go to `content.py` and change the variable `input_fns`.

`FILE` Components

- There's a `Path` field in `config.ini` to specify the file path.

- The first line of the file needs to be `1`, or the rest of the file will not be read.

### Components

`Foobar2K Now Playing`

- Setup

    - Install `foo_np_simple`.
    
    - Setup the output using `$crlf()` to separate lines(outputs) in FB2K. 
    
        - Remember that the first line will indicate if the file will be read. Anything besides `1` will skip the read.
        
    - Copy the file output path, and paste it under `Foobar2K/Path` in `config.ini`.
    
`Static Text`

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
    
`Youtube Data API`
   
- Setup
   
    - `YT_VIDEO_ID`: The video ID to track the current viewers
    
    - `YT_API_KEY`: The API key acquired using Google Cloud Console
    
- Note

    - Output will be skipped if the current viewer is 0 or inaccessible.

### Endpoints

#### `/`

Marquee with styles applied.

#### `/dt`

Current timestamp expression with styles applied.

Automatically update once a second.

##### Parameter

- `suffix`: Suffix to be attached after the current datetime expression

#### `/content/marquee`

Pure text of the next content of the marquee.

#### `/content/dt`

Pure text of the current time.

##### Parameter

- `suffix`: Suffix to be attached after the current datetime expression