# Bryan Popka's Challenge 1. Weather Pattern Code

## Approach Used
Similar to the approach used for Translations, I used VSCode CoPilot (Claude Sonnet 4.5) to produce a list of the most common inclement weather terms in English. I then had Claude translate that list to the other languages so I could analyze all 4. From there I looked at the total message count per day vs. the number of messages mentioning the inclement weather terms for that day.

# Notebooks:
    1. InclementWeatherMessagePatterns - Analysis and charts of the top inclement weather terms across all the languages, with a frequency timeseries analysis showing total messages per day vs. those mentioning the weather terms. I also performed analysis comparing total message frequency by hour of the day vs. those messages mentioning inclement weather to see if there was a change in message frequency throught the day when weather gets bad, but both lines are the chart followed a very similar trend, indicating no behavioral impact from the weather.