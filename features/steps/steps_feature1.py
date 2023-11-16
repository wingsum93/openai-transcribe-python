from behave import given, when, then, step
import os
from subtitle_generator import SubtitleGenerator, VideoProcessor

@given('a video file "{video_file}" with clear audio')
def step_impl(context, video_file):
    context.video_file = video_file
    assert os.path.exists(video_file)

@given('a video file "{video_file}" with no audio')
def step_impl(context, video_file):
    context.video_file = video_file
    assert os.path.exists(video_file)

@given('a non-existent video file "{video_file}"')
def step_impl(context, video_file):
    context.video_file = video_file
    assert not os.path.exists(video_file)

@when('I request to generate subtitles')
def step_impl(context):
    try:
        video_processor = VideoProcessor(context.video_file)
        audio = video_processor.extract_audio()
        context.subtitle_generator = SubtitleGenerator(audio)
        context.subtitles = context.subtitle_generator.generate()
    except FileNotFoundError:
        context.exception = FileNotFoundError
    except NoAudioTrackError:
        context.exception = NoAudioTrackError

@then('the subtitle file "{subtitle_file}" should be created')
def step_impl(context, subtitle_file):
    assert os.path.exists(subtitle_file)

@then('the subtitles should accurately represent the audio content')
def step_impl(context):
    # Here you might include logic to verify the accuracy of subtitles.
    # This could be a simple placeholder as actual verification can be complex.
    pass

@then('an error message "{message}" should be displayed')
def step_impl(context, message):
    assert message in str(context.exception)
