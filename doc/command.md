# Command for the project

## Mac

#### process one youtube
```
python subtitle_generator/cli.py process-youtube "https://youtu.be/EWWO5Igp0Ko?si=5vwghOmckqCs_W4e" -m=medium -sl=zh -es 
```

#### process multiple youtube videos
```
python subtitle_generator/cli.py process-many-youtube "temp/batch-youtube.txt" -m=medium -sl=zh -es
```

#### process local video
```
python subtitle_generator/cli.py process-video "sample/Easy Cantonese 3.mp4" --model=medium -sl=zh --enable_srt
```
#### process local mp3
```
python subtitle_generator/cli.py process-mp3 "sample/01. 黄昏のスタアライト.mp3" -m=medium -sl=ja -tl=zh -es
```

#### process multiple video
```
python subtitle_generator/cli.py process-many-video "temp/batch-video.txt" -m=medium -sl=zh -es
```

#### Process Multiple Japanese files with Translation
```
python subtitle_generator/cli.py process-many-video "temp/batch-video.txt" -m=medium -sl=ja -tl=zh -es
```

#### Process Multiple English files with Translation
```
python subtitle_generator/cli.py process-many-video "temp/batch-video.txt" -m=medium -sl=en -tl=zh -es
```