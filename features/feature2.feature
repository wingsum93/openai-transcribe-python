Feature: Subtitle Customization

  As a user of the subtitle generator
  I want to customize the output of the subtitles
  So that I can adjust the timing and format to suit my preferences

  Scenario: Adjusting the timing offset of subtitles
    Given a video file "video_with_offset.mp4"
    And the default subtitle timing is out of sync
    When I adjust the timing offset to "2 seconds"
    And request to generate subtitles
    Then the subtitle file "video_with_offset.srt" should be created
    And the subtitles should be in sync with the audio

  Scenario: Selecting a specific subtitle format
    Given a video file "video_for_format.mp4"
    When I select the "VTT" subtitle format
    And request to generate subtitles
    Then the subtitle file "video_for_format.vtt" should be created
    And the file format should be in WebVTT format

  Scenario: Handling invalid timing offset input
    Given a video file "video_with_invalid_offset.mp4"
    When I input an invalid timing offset "xyz"
    And request to generate subtitles
    Then an error message "Invalid timing offset" should be displayed

  Scenario: Choosing an unsupported subtitle format
    Given a video file "video_with_unsupported_format.mp4"
    When I select an unsupported subtitle format "TXT"
    And request to generate subtitles
    Then an error message "Unsupported subtitle format" should be displayed
