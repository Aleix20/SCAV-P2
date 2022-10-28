import os


def trim(in_file, out_file, start, end):
    if os.path.exists(out_file):
        os.remove(out_file)
    # command to trim the video in our case only working until 59 seconds
    command = 'ffmpeg -ss 00:00:' + str(start) + ' -i ' + in_file + ' -t 00:00:' + str(end) + ' -c copy ' + out_file
    os.system(command)


def informationVideo(input_file):
    if os.path.exists("out.txt"):
        os.remove("out.txt")
    command = 'ffmpeg -i ' + input_file + ' 2> out.txt'
    os.system(command)
    with open("out.txt") as file:
        for line in file:
            if line.startswith("Input") or "Stream" in line:
                # Save bitrate of the audio
                if "Audio" in line:
                    global bitrate
                    splittedline = line.split(",")
                    bitrate = splittedline[len(splittedline) - 1]
                    bitrate = bitrate.split(" ")[1]
                print(line)
    os.remove("out.txt")


def newBBBContainer():
    trim("BBB.mp4", "BBB1min.mp4", 0, 59)
    if os.path.exists("BBB1min.mp3"):
        os.remove("BBB1min.mp3")
    if os.path.exists("BBB1min.aac"):
        os.remove("BBB1min.aac")
    if os.path.exists("multiaudio.mp4"):
        os.remove("multiaudio.mp4")
    # extract mp3 from 1 min video in stereo
    command = 'ffmpeg -i BBB1min.mp4 -vn -ac 2 BBB1min.mp3'
    os.system(command)
    # Extract aac audio with -5k bitrate compared to the input
    command = 'ffmpeg -i BBB1min.mp4 -vn -b:a ' + str(int(bitrate) - 5) + 'k -acodec copy BBB1min.aac'
    os.system(command)
    # Package 1 min video and all the audio files in one
    command = 'ffmpeg -i BBB1min.mp4 -i BBB1min.mp3 -i BBB1min.aac -map 0 -map 1 -map 2 -metadata:s:a:0 ' \
              'language=\"audio1\" ' \
              '-metadata:s:a:1 language=\"audio2\" -metadata:s:a:2 language=\"audio3\"  -codec copy multiaudio.mp4 '
    os.system(command)


def resizeVideo(input_file, width, height):
    if os.path.exists("output_" + str(width) + ":" + str(height) + ".mp4"):
        os.remove("output_" + str(width) + ":" + str(height) + ".mp4")
    # Command that allow us to scale to any size
    command = 'ffmpeg -i ' + input_file + ' -vf scale=' + str(width) + ':' \
              + str(height) + ',setsar=1:1 output_' + str(width) + ':' + str(height) + '.mp4'
    os.system(command)


def checkAudioTracks(input_file):
    if os.path.exists("out.txt"):
        os.remove("out.txt")
    if os.path.exists("out1.txt"):
        os.remove("out1.txt")
    command = 'ffmpeg -i ' + input_file + ' 2>out.txt'
    os.system(command)
    # Save only video and audio matches
    command = 'cat out.txt | grep \'Stream\' | cut -d " " -f 5,6> out1.txt'
    os.system(command)
    os.remove("out.txt")
    audioResult = []
    # Save all the audio codecs
    with open("out1.txt") as file:
        for line in file:
            if line.__contains__("Audio"):
                line = line.split(" ")
                audioResult.append(line[1])
    os.remove("out1.txt")
    if audioResult.__contains__("aac\n"):
        print("Contains a aac audio track")
        print("Broadcasting could be : DVB, ISDB or DTMB")
    if audioResult.__contains__("mp3\n"):
        print("Contains a mp3 audio track")
        print("Broadcasting could be : DVB or DTMB")
    if audioResult.__contains__("ac3\n"):
        print("Contains a ac3 audio track")
        print("Broadcasting could be : DVB, ATSc or DTMB")
    if audioResult.__contains__("mp2\n"):
        print("Contains a mp2 audio track")
        print("Broadcasting could be : DTMB")
    if audioResult.__contains__("dra\n"):
        print("Contains a dra audio track")
        print("Broadcasting could be : DTMB")


informationVideo("BBB1min.mp4")
newBBBContainer()
resizeVideo("BBB1min.mp4", 320, 240)
checkAudioTracks("multiaudio.mp4")
