---
title: "Twitter analysis of the West Indian Carnival"
author: "Robin Lovelace"
date: "27/09/2014"
output:
  html_document: default
  pdf_document:
    fig_caption: yes
---

## Introduction

The West Indian Carnival takes place in late August each year in Leeds, attracting tens of
thousands of people to Chapeltown, a multi-cultural area to the north of the city centre.
In 2014 the event was held from the 17^th^ until the 25^th^ of August.

This report investigates what social media data might be able to tell us about the event,
above and beyond official estimates of the turnout.

## The data

As a baseline dataset, we used all geotagged tweets in the UK between the 20^th^ August
until the 28^th^ August. This consisted of 10 raw input `.json` files, harvested using
the Python-based tweet streamer
[tweepy](https://github.com/Robinlovelace/tweepy), and occupying **30 Gb** of hard disk space.
The time window extended before and after the carnival to enable identification its
social media impact relative to the baseline.

The area of particular interest was the zone of the routes, shown in the figure below.
All tweets sent within this zone were filtered out from the national dataset and then
analysed. The script
['BigLoad.R'](https://github.com/Robinlovelace/tweepy/blob/master/BigLoad.R)
was used to extract tweets within the study area,
reducing the size of the dataset from 30 Gb to a more manageable 400 Kb,
1/75,000^th^ the size of the original dataset!

![The carnival boundary based on online maps]("carnival-bounds.png")

## Analysis

The filtered tweets are stored in 'output.csv'. There were
2,268 tweets were recorded in the study area.


```
## Warning: cannot open file
## '/nfs/foe-fs-01_users/georl/repos/tweepy/Carnival/output.csv': No such
## file or directory
```

```
## Error: cannot open the connection
```

Interestingly, there were no more tweets sent during the carnival than
usual.


```
## Error: object 'ct' not found
```

```
## Error: object 'ct' not found
```

When we look at tweets containing 'carnival, there is a social media signal, which
peaks on Monday 25^th^. 77 tweets contained the word Carnival (3%), far above the national
average of tweets containing this word, showing the event had a substantial social media footprint.


```
## Error: object 'ct' not found
```

```
## Error: object 'cn' not found
```

## Spatial analysis

A 'ground truth' on the location of the tweets was undertaken by plotting all
messages in the study area with tweets containing the word "carnival".
The results clearly show that people tweeting about the carnival tended to
be located in some of its focal points, in Potternewton park (northeast of the map)
and on Chapeltown road (in the centre of the map).


```
## Error: object 'ct' not found
```

```
## Error: object 'geoc' not found
```

```
## Error: object 'geoc' not found
```

```
## Error: error in evaluating the argument 'obj' in selecting a method for function 'bbox': Error: object 'geoc' not found
```

It would be interesting to see how the number of people tweeting about the event fluctuated
over time, but there are insufficient data points for space-time analysis at this stage.

## Text

After some preprocessing to remove punctuation, 'stopwords' (e.g. 'and', 'his', 'to'),
html links and blank space, the average number of words per tweet was found to be just
under 10.


```
## Error: object 'geoc' not found
```

```
## Error: object 'ct' not found
```

```
## Error: object 'ct' not found
```

```
## Error: object 'ct' not found
```

```
## Error: object 'ct' not found
```

```
## Error: object 'ct' not found
```

```
## Error: object 'ct' not found
```

```
## Error: object 'ct' not found
```

```
## Error: object 'wordlist' not found
```

```
## Error: object 'words_per_tweet' not found
```

The most frequently used words overall, and in those containing 'carnival'
are shown below.


```
## Error: object 'wordlist' not found
```

```
## Error: object 'all_words' not found
```

```
## Error: object 'all_words' not found
```

```
## Error: object 'unique_words' not found
```

```
## Error: there is no package called 'wordcloud'
```

```
## Error: could not find function "wordcloud"
```


```
## Error: object 'ct' not found
```

```
## Error: object 'wordlist' not found
```

```
## Error: object 'wordlist' not found
```

```
## Error: object 'all_words' not found
```

```
## Error: object 'all_words' not found
```

```
## Error: object 'unique_words' not found
```

```
## Error: there is no package called 'wordcloud'
```

```
## Error: could not find function "wordcloud"
```





