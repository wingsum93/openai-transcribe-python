Feature: Subtitle Generation

  As a user of the subtitle generator
  I want to generate subtitles from a video file
  So that I can have accurate subtitles for my video content

  Scenario: Generating subtitles from a video file with clear audio
    Given a video file "clear_audio_video.mp4" with clear audio
    When I request to generate subtitles
    Then the subtitle file "clear_audio_video.srt" should be created
    And the subtitles should accurately represent the audio content

  Scenario: Handling a video file with no audio
    Given a video file "no_audio_video.mp4" with no audio
    When I request to generate subtitles
    Then an error message "No audio track found" should be displayed

  Scenario: Handling a non-existent video file
    Given a non-existent video file "non_existent.mp4"
    When I request to generate subtitles
    Then an error message "Video file not found" should be displayed
