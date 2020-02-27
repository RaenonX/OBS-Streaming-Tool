# OBS Streaming Tool

This was created to enable marquee (with pause) effect in OBS.

### Notes

- Developed under Python 3.8.

- Running from multiple sources will result in some contents being skipped.

### Usage

1. Run `py -m flask run`.

    - Be sure to install `flask` in your Python environment.

2. Create a `Browser` source with the URL which flask is running on. Default to `http://127.0.0.1/5000`.

    - The height is defaulted to 72px with the font size of 28px. Approximately 2 lines max without weird output.
    
    - All things above are customizable by modifying `templates/main.html`.

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
    
`Youtube Data API`
   
- Setup
   
    - `YT_VIDEO_ID`: The video ID to track the current viewers
    
    - `YT_API_KEY`: The API key acquired using Google Cloud Console
    
- Note

    - Output will be skipped if the current viewer is 0 or inaccessible.