# Tracking

## Prompts

### Session 1 Prompts

1.  I want to create a web app that a user can upload a file and the web app will respond with metrics on the count of pixel by color. The max upload should be 100 MB and the file shouldn't be saved. I want this app to be dockerized. If there are other metrics about color pixel count that are interesting include them.
2.  settings.MAX_UPLOAD_SIZE_BYTES is used for the check here. I see both MAX_UPLOAD_SIZE_MB and MAX_UPLOAD_SIZE_BYTES in config.py. I also see docker compose setting MAX_UPLOAD_SIZE_MB. It seems to me we only need one of those and which ever one we choose need to make sure its what docker compose uses.

### Session 2 Prompts

1.  I want to expand the table to be top 25. I would like to display the picture above the table. I would like to have two transforming operations. One that replaces a pixel with the closest color in the top 25. If its a tie use the color that appears more frequently. The other feature should turn all pixels matching colors to white. The transformed image should be next to the original image for comparison.

## Metrics

- **Number of Prompts needed:** 3
- **Time:** 30 minutes
- **Success:** Successful - I had to do very little other than prompt. It had a little trouble with limiting image size but was easily corrected with another prompt. Because Jules actually runs the code it was able to produce images of what the outcome would look like which was really useful. I thought Jules was a little lacking on documentation like the README and how to actually run the app.
- **Link:** https://chuck.rocks/pixel-counter

## Environment

- **Tools:** Jules
- **Model:** gemini-3.0-pro

## Pre-existing Files

- `.gitignore`
- `AGENTS.md`
- `TRACKING.md`
